#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Copyright (c) 2025 DeepTouch - 瞬恒智能科技（北京）有限公司
Author: max
Time: 2025-09-25
All rights reserved.

This software is proprietary and confidential. Unauthorized copying,
distribution, or use of this software, via any medium, is strictly prohibited.
"""

import time
import threading
from typing import Dict, Optional, List
import logging

import numpy as np
from scipy.spatial.transform import Rotation as R
from concurrent.futures import ThreadPoolExecutor
import sys
import os
# Import the provided robot interface
sys.path.append('/workspace/deeptouch/src/RM_API2/Python') 
from Robotic_Arm.rm_robot_interface import *

class ArmControlMode:
    """Robot arm control modes"""
    NoMotion = 0
    JOINT_POSITION = 1
    ABSOLUTE_CART_POSE = 2
    OSC_CARTESIAN_POSE = 3


class RobotController:
    """Controller for multiple robotic arms"""
    
    def __init__(self, robot_configs: dict):
        print("🔥 [DEBUG] RobotController 正在初始化... 代码修改已生效！")
        self.robot_configs = robot_configs
        self.logger = logging.getLogger("RobotController")
        
        # Multiple robot connections
        self.robot_arms = {}
        self.robot_handles = {}
        self.connected_arms = set()
        
        # Robot states for each arm
        self.state_locks = {arm_name: threading.Lock() for arm_name in robot_configs.keys()}
        self.latest_states = {arm_name: {} for arm_name in robot_configs.keys()}
        
        # State callbacks for each arm
        self.state_callbacks = {}
        
        # 创建一个夹爪控制的线程池
        self.executor = ThreadPoolExecutor(max_workers=10)

        # Initialize each arm
        for arm_name, config in robot_configs.items():
            self.state_locks[arm_name] = threading.Lock()
            self.latest_states[arm_name] = None

        connection_results = self.connect_all()
        connected_arms = [arm for arm, success in connection_results.items() if success]
        self.connected_arms.update(connected_arms)

        self.ip_to_arm_map = self.create_ip_to_arm_map()

        self.setup_callbacks()
        time.sleep(0.1)  # Wait for callbacks to initialize

        if not connected_arms:
            self.logger.error("No robot arms connected, cannot start recording")
            return
        self.logger.info(f"Connected arms: {connected_arms}")
    
    def create_ip_to_arm_map(self) -> dict:
        """ 创建一个 IP 地址到机械臂名称的映射 """
        return {config['ip']: arm_name for arm_name, config in self.robot_configs.items()}
    
    def find_arm_name_by_ip(self, target_ip: str) -> str:
        """ 根据 IP 地址查找对应机械臂的名称 """
        return self.ip_to_arm_map.get(target_ip, "未找到对应的机械臂")

    def connect_all(self) -> Dict[str, bool]:
        """Connect to all configured robots"""
        results = {}
        
        for arm_name, config in self.robot_configs.items():
            results[arm_name] = self.connect_arm(arm_name, config)
            
        return results
    
    def connect_arm(self, arm_name: str, config: dict) -> bool:
        """Connect to a specific robot arm"""
        try:
            # Initialize robot in triple thread mode
            self._init_config(arm_name, config)
            
            self.connected_arms.add(arm_name)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to connect to {arm_name}: {e}")
            return False
    
    def setup_callbacks(self):
        """Set up individual callbacks for each arm in separate threads."""
        for arm_name in self.connected_arms:
            # self._setup_udp_streaming(arm_name, self.robot_configs[arm_name])
            self._setup_udp_streaming(arm_name, self.robot_configs[arm_name])
            self.executor.submit(self._initialize_arm_callback, arm_name)

    def _initialize_arm_callback(self, arm_name: str):
        """Initialize the state callback for the specified arm in a separate thread."""
        def state_callback_func(data):
            """Callback function to handle state updates for a specific arm."""
            self._on_robot_state_update(arm_name, data, self.robot_configs[arm_name].get('has_gripper', False))
        
        state_callback = rm_realtime_arm_state_callback_ptr(state_callback_func)
        self.state_callbacks[arm_name] = state_callback
        self.robot_arms[arm_name].rm_realtime_arm_state_call_back(state_callback)


    def shutdown_executor(self):
        """关闭夹爪控制线程池，如果存在的话"""
        if self.executor is not None:
            self.executor.shutdown(wait=True)
            self.executor = None
            
    def _init_config(self, arm_name, config):
        robot_ip = config.get('ip', '192.168.1.18')
        robot_port = config.get('port', 8080)
        robot_arm = RoboticArm(rm_thread_mode_e.RM_TRIPLE_MODE_E)

        robot_handle = robot_arm.rm_create_robot_arm(robot_ip, robot_port)
        self.logger.info(f"Connected to {arm_name} at {robot_ip}:{robot_port}, handle: {robot_handle.id}")
        
        # Store connections
        self.robot_arms[arm_name] = robot_arm
        self.robot_handles[arm_name] = robot_handle

        robot_arm.rm_change_work_frame("World")
        time.sleep(0.2)
        robot_arm.rm_set_tool_voltage(3)
        time.sleep(0.2)
        robot_arm.rm_change_tool_frame(config.get('tool_frame_id', 'gripper'))
        time.sleep(0.2)
        
        robot_arm.rm_algo_set_angle(0, -60, 0)

        rm_algo_init_sys_data(rm_robot_arm_model_e.RM_MODEL_RM_75_E, rm_force_type_e.RM_MODEL_RM_ISF_E)
        coord_work = rm_frame_t()
        coord_work.pose.position.x = 0.0
        coord_work.pose.position.y = 0.0
        coord_work.pose.position.z = 0.0
        coord_work.pose.euler.rx   = 0.0
        coord_work.pose.euler.ry   = 0.0
        coord_work.pose.euler.rz   = 0.0
        robot_arm.rm_algo_set_workframe(coord_work)

    def disconnect_all(self):
        """Disconnect from all robots"""
        for arm_name in list(self.connected_arms):
            self.disconnect_arm(arm_name)
    
    def disconnect_arm(self, arm_name: str):
        """Disconnect from a specific robot"""
        if arm_name in self.robot_arms:
            try:
                self.robot_arms[arm_name].rm_delete_robot_arm()
                del self.robot_arms[arm_name]
                del self.robot_handles[arm_name]
                self.connected_arms.discard(arm_name)
                self.logger.info(f"Disconnected from {arm_name}")
            except Exception as e:
                self.logger.error(f"Error disconnecting from {arm_name}: {e}")
    
    def _setup_udp_streaming(self, arm_name: str, config: dict):
        """Setup UDP streaming for real-time robot state"""
        # Configure UDP settings
        udp_config = config.get('udp', {})
        has_gripper = config.get('has_gripper', True)

        # 🟢【添加这三行调试打印】
        target_ip = udp_config.get('target_ip', '192.168.1.104')
        port = udp_config.get('port', 8089)
        print(f"🔍 [DEBUG] 正在尝试配置 {arm_name} 推送目标 -> IP: {target_ip}, Port: {port}")

        custom = rm_udp_custom_config_t()
        custom.joint_speed = 1  # Enable joint speed reporting
        custom.lift_state = 0
        custom.expand_state = 1
        custom.arm_current_status = 1

        udp_push_config = rm_realtime_push_config_t(
            udp_config.get('cycle_time', 10),  # 10ms cycle
            True,  # Enable
            udp_config.get('port', 8089),
            0,  # Force coordinate system
            udp_config.get('target_ip', '192.168.1.104'),
            custom
        )
        
        # Set UDP configuration
        result = self.robot_arms[arm_name].rm_set_realtime_push(udp_push_config)
        # 🟢【添加这一行结果检查】
        print(f"📡 [DEBUG] {arm_name} 推送配置结果 (0代表成功): {result}")
        self.logger.info(f"UDP streaming setup for {arm_name}: {result}")
        
        # # Register callback for state updates
        # def state_callback_func(data):
        #     # if arm_name == 'left_arm':
        #     #     self._on_robot_state_update(arm_name, data, success=True)
        #     # elif arm_name == 'right_arm':
        #     #     self._on_robot_state_update(arm_name, data, success=True)
        #     self._on_robot_state_update(arm_name, data, has_gripper)
        
        # state_callback = rm_realtime_arm_state_callback_ptr(state_callback_func)
        # self.state_callbacks[arm_name] = state_callback
        # self.robot_arms[arm_name].rm_realtime_arm_state_call_back(state_callback)
    
    def _on_robot_state_update(self, arm_name: str, data, has_gripper: bool):
        """Handle robot state updates from UDP stream"""
        try:
            received_arm_ip = data.arm_ip.decode('utf-8') if isinstance(data.arm_ip, bytes) else data.arm_ip
            arm_name = self.find_arm_name_by_ip(received_arm_ip)
            # print("received_arm_ip", arm_name, received_arm_ip)

            with self.state_locks[arm_name]:
                # 1. 基本信息
                # 2. 获取该 arm_name 对应的预期 IP 地址
                expected_arm_ip = self.robot_configs[arm_name]['ip']

                # if received_arm_ip != expected_arm_ip:
                #     return

                arm_status = data.arm_current_status
                error_code = data.errCode

                # 2. 关节状态 - numpy数组输出
                joint_status = data.joint_status.to_dict()
                joint_positions = np.array(joint_status['joint_position'], dtype=np.float32)
                joint_speeds = np.array(joint_status['joint_speed'], dtype=np.float32)
                joint_currents = np.array(joint_status['joint_current'], dtype=np.float32)
                joint_temperatures = np.array(joint_status['joint_temperature'], dtype=np.float32)
                
                # 3. 末端执行器位姿 - numpy数组输出
                waypoint = data.waypoint.to_dict()
                
                # 位置信息
                position_dict = waypoint['position']
                position = np.array([
                    position_dict['x'],
                    position_dict['y'], 
                    position_dict['z']
                ], dtype=np.float32)
                
                # 四元数信息
                quaternion_dict = waypoint['quaternion']
                quaternion = np.array([
                    quaternion_dict['x'],
                    quaternion_dict['y'],
                    quaternion_dict['z'],
                    quaternion_dict['w']
                ], dtype=np.float32)
                
                # 完整位姿 [x, y, z, qx, qy, qz, qw]
                pose_quaternion = np.concatenate([position, quaternion])
                
                # 欧拉角信息
                euler_dict = waypoint['euler']
                euler = np.array([
                    euler_dict['rx'],
                    euler_dict['ry'],
                    euler_dict['rz']
                ], dtype=np.float32)

                pose_euler = np.concatenate([position, euler])
    
                # 4. 力传感器信息 - numpy数组输出
                force_sensor = data.force_sensor.to_dict()
                force_current = np.array(force_sensor['force'], dtype=np.float32)
                zero_force = np.array(force_sensor['zero_force'], dtype=np.float32)

                # 5. 夹爪状态
                gripper_info = {}
                if has_gripper:
                    gripper_status_code, gripper_dict = self._get_gripper_state(arm_name)

                    mode = gripper_dict.get('mode', 0)
                    gripper_close = -1
                    # 根据模式判断夹爪状态
                    if mode in [2, 4, 3, 6]:  # 闭合状态
                        gripper_close = 1
                
                    gripper_info = {
                        'status_code': gripper_status_code,
                        'enable_state': gripper_dict.get('enable_state', 0),
                        'status': gripper_dict.get('status', 0),
                        'error': gripper_dict.get('error', 0),
                        'mode': gripper_dict.get('mode', 0),
                        'current_force': gripper_dict.get('current_force', 0),
                        'temperature': gripper_dict.get('temperature', 0),
                        'actpos': gripper_dict.get('actpos', 0),
                        'gripper_close': gripper_close
                    }
                
                state = {
                    'timestamp': time.time(),
                    'arm_name': arm_name,
                    'arm_ip': received_arm_ip,
                    'arm_status': arm_status,
                    'error_code': error_code,
                    'joint_positions': joint_positions,
                    'joint_speeds': joint_speeds,
                    'joint_currents': joint_currents,
                    'joint_temperatures': joint_temperatures,
                    'pose_quaternion': pose_quaternion,
                    'pose_euler': pose_euler,
                    'force_current': force_current,
                    'zero_force': zero_force,
                    'gripper_info': gripper_info
                }
                    
                # Update latest state
                self.latest_states[arm_name] = state
                
        except Exception as e:
            self.logger.error(f"Error processing robot state for {arm_name}: {e}")
    
    def get_state(self, arm_name: str) -> Optional[Dict]:
        """Get current robot state for specific arm"""
        with self.state_locks[arm_name]:
            return self.latest_states[arm_name]
    
    def get_all_states(self) -> Dict[str, Optional[Dict]]:
        """Get states for all arms"""
        states = {}
        for arm_name in self.connected_arms:
            states[arm_name] = self.get_state(arm_name)
        return states
    
    def _get_gripper_state(self, arm_name: str):
        """安全获取夹爪状态"""
        try:
            if arm_name not in self.robot_arms:
                return -1, {}
                
            result = self.robot_arms[arm_name].rm_get_gripper_state()
            
            if isinstance(result, tuple):
                if len(result) >= 2:
                    status_code, data = result
                    if isinstance(data, dict):
                        return status_code, data
                    else:
                        return status_code, {}
                else:
                    return result[0] if len(result) > 0 else -1, {}
                    
            elif hasattr(result, 'to_dict'):
                # 如果有 to_dict 方法
                return 0, result.to_dict()
                
            elif isinstance(result, dict):
                # 如果直接是字典
                return 0, result
                
            else:
                # 其他情况
                return -1, {}
                
        except Exception as e:
            self.logger.warning(f"Failed to get gripper state for {arm_name}: {e}")
            return -1, {}
    
    def initialize_arm_pose(self, arm_name: str) -> bool:
        """Initialize robot arm to predefined pose"""
        if arm_name not in self.connected_arms or arm_name not in self.robot_arms:
            return False
        
        try:
            init_joint_positions = self.robot_configs[arm_name].get('init_pose', {}).get('joint_positions', None)

            if init_joint_positions is not None:
                self.send_command(arm_name, ArmControlMode.JOINT_POSITION, np.array(init_joint_positions), gripper_close=False)
            else:
                self.logger.warning(f"No initial joint positions defined for {arm_name}")
                return False
        except Exception as e:
            self.logger.error(f"Error initializing pose for {arm_name}: {e}")
            return False

    def stop_arm(self, arm_name: str):
        try:
            robot_arm = self.robot_arms[arm_name]
            robot_arm.rm_set_arm_stop()
        except Exception as e:
            self.logger.error(f"Error stopping arm {arm_name}: {e}")
    
    def get_infer_state(self, arm_name: str) -> Optional[np.ndarray]:
        """获取机械臂当前位姿的轴角表示"""
        if arm_name not in self.connected_arms or arm_name not in self.robot_arms:
            return None
        
        try:
            state = self.robot_arms[arm_name].rm_get_current_arm_state()
            current_pose_eular = state[1]["pose"]

            current_t = current_pose_eular[0:3]
            current_rotation = (R.from_euler("xyz", current_pose_eular[3:])).as_matrix()

            current_axis_angle = R.from_matrix(current_rotation).as_rotvec()

            gripper_close = -1
            if self.has_gripper:
                gripper_status_code, gripper_dict = self._get_gripper_state(arm_name)

                mode = gripper_dict.get('mode', 0)
                # 根据模式判断夹爪状态
                if mode in [2, 4, 6]:  # 闭合状态
                    gripper_close = 1
            
            get_infer_state = np.concatenate([current_t, current_axis_angle, gripper_close, -gripper_close])

            return get_infer_state

        except Exception as e:
            self.logger.error(f"Error getting pose axis angle for {arm_name}: {e}")
            return None



    def send_command(self, arm_name: str, command: ArmControlMode, data: np.ndarray, gripper_close=False) -> bool:
        """Send command to specific robot"""
        if arm_name not in self.connected_arms or arm_name not in self.robot_arms:
            return False
        
        try:
            robot_arm = self.robot_arms[arm_name]

            if command == ArmControlMode.JOINT_POSITION:
                joint_pos = data                
                ret = robot_arm.rm_movej(joint_pos.tolist(), self.robot_configs[arm_name].get("movej_velocity", 15.0), 0, 0, True)
            
            elif command == ArmControlMode.ABSOLUTE_CART_POSE:
                # 若位姿列表长度为7则认为使用四元数表达位姿，长度为6则认为使用欧拉角表达位姿
                ret = robot_arm.rm_movep_follow(data.tolist())
                pass            
            elif command == ArmControlMode.OSC_CARTESIAN_POSE:
                # [x, y, z, qx, qy, qz, qw]
                # 若位姿列表长度为7则认为使用四元数表达位姿，长度为6则认为使用欧拉角表达位姿
                # current_pose_quat = self.latest_states[arm_name]["pose_quaternion"]
                # delta_pose_axis_angle = data

                # delta_t = delta_pose_axis_angle[0:3]
                # current_t = current_pose_quat[0:3]
                
                # delta_rotation = R.from_rotvec(delta_pose_axis_angle[3:] ).as_matrix()
                # current_rotation = R.from_quat(current_pose_quat[3:]).as_matrix()

                # current_tf = Tf.from_components(current_t, current_rotation)
                # delta_tf = Tf.from_components(delta_t, delta_rotation)
                
                # target_tf = current_tf * delta_tf
                # target_t, target_rotation = target_tf.as_components()
                # target_quat = R.from_matrix(target_rotation).as_quat()
                # target_pose = np.concatenate([target_t, target_quat])


                # current_pose_quat = self.latest_states[arm_name]["pose_quaternion"]
                
                state = robot_arm.rm_get_current_arm_state()
                current_pose_eular = state[1]["pose"]
                delta_pose_axis_angle = data

                delta_t = delta_pose_axis_angle[0:3]
                current_t = current_pose_eular[0:3]

                delta_rotation = R.from_rotvec(delta_pose_axis_angle[3:]).as_matrix()
                current_rotation = (R.from_euler("xyz", current_pose_eular[3:])).as_matrix()

                target_t = current_t + delta_t.T
                target_rotation = delta_rotation @ current_rotation 
                target_euler = R.from_matrix(target_rotation).as_euler("xyz", degrees=False)

                target_pose = np.concatenate([target_t, target_euler])



                ret = robot_arm.rm_movep_follow(target_pose.tolist())
                # ret = 0  # 假设命令发送成功
            
            # 异步更新夹爪状态
            if gripper_close is not None and self.robot_configs[arm_name].get('has_gripper', True):
                self.executor.submit(self._update_gripper_state, arm_name, gripper_close)

            return ret == 0

        except Exception as e:
            self.logger.error(f"Error sending command to {arm_name}: {e}")
            return False

    def _update_gripper_state(self, arm_name, gripper_close):
        """更新夹爪状态的线程执行方法"""
        try:
            robot_arm = self.robot_arms[arm_name]

            if gripper_close:
                robot_arm.rm_set_gripper_pick_on(1000, self.robot_configs[arm_name].get('gripper_force', 350), False, 0)
            else:
                robot_arm.rm_set_gripper_release(1000, False, 0)
        except Exception as e:
            self.logger.error(f"Error updating gripper state: {e}")


# 测试代码
if __name__ == "__main__":
    import signal
    import sys
    from datetime import datetime
    
    # 双臂配置
    robot_configs = {
        'left_arm': {
            'ip': '192.168.0.18',
            'port': 8080,
            'dof': 7,
            'has_gripper': True,
            'udp': {
                'cycle_time': 2,
                'port': 8008,
                'target_ip': '192.168.0.10'
            },
            'tool_frame_id': "gripper",
            'gripper_force': 350,
            'init_pose': {
                'joint_positions': [16.737,52.108,29.185,83.404,18.195,90.774,87.215]
            },
            'movej_velocity': 15
        },
        'right_arm': {
            'ip': '192.168.0.19',
            'port': 8080,
            'dof': 7,
            'has_gripper': True,
            'udp': {
                'cycle_time': 2,
                'port': 8009,
                'target_ip': '192.168.0.10'
            },
            'tool_frame_id': "gripper",
            'gripper_force': 350,
            'init_pose': {
                'joint_positions': [5.875,-72.779,93.664,84.180,11.549,94.480,47.923]
            },
            'movej_velocity': 15
        }
    }
    
    def signal_handler(sig, frame):
        """处理中断信号"""
        if 'controller' in globals():
            controller.disconnect_all()
        sys.exit(0)
    
    def print_multi_arm_state(states):
        """打印多臂状态"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}]")
        
        for arm_name, state in states.items():
            if state:
                joints = state.get('joint_positions', [])[:6]
                pos = state.get('pose_euler', [])[:3]
                gripper = state.get('gripper_info', {}).get('gripper_close', 0)
                
                j_str = ",".join([f"{j:.1f}" for j in joints])
                p_str = ",".join([f"{p:.3f}" for p in pos])
                
                print(f"  {arm_name:>10}: J:[{j_str}] P:[{p_str}] G:{gripper}")
            else:
                print(f"  {arm_name:>10}: ⚠️  等待数据...")
        print("-" * 60)
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    
    # 创建多臂控制器
    print("🚀 启动多臂机器人控制器...")
    controller = RobotController(robot_configs)
    
    # 连接所有机器人
    # results = controller.connect_all()
    
    # print("连接结果:")
    # for arm_name, success in results.items():
    #     status = "✅ 成功" if success else "❌ 失败"
    #     print(f"  {arm_name}: {status}")
    
    # if not any(results.values()):
    #     print("❌ 所有机器人连接失败")
    #     sys.exit(1)

    # while True:
    #     # print("等待机械臂状态数据...-----------------------------")
    #     time.sleep(0.1)
    #     states = controller.get_all_states()
    #     right_test_joint_positions = states['right_arm']['joint_positions']
    #     left_test_joint_positions = states['left_arm']['joint_positions']
    #     # print("right", right_test_joint_positions)
    #     print("left", left_test_joint_positions)
    #     time.sleep(0.1)

    states = controller.get_all_states()

    right_pose_quat = states['right_arm']['pose_quaternion']

    success = controller.initialize_arm_pose('right_arm')

    states = controller.get_all_states()


    test_joint_positions = states['right_arm']['joint_positions']
    test_joint_positions[6] = test_joint_positions[6] + 5.0 
    controller.send_command('right_arm', ArmControlMode.JOINT_POSITION, np.array(test_joint_positions), gripper_close=True)
    states = controller.get_all_states()
    time.sleep(2)


    test_pose_eular = states['right_arm']['pose_euler']
    test_pose_eular[0] = test_pose_eular[0] + 0.03
    controller.send_command('right_arm', ArmControlMode.ABSOLUTE_CART_POSE, np.array(test_pose_eular), gripper_close=False)

    time.sleep(1)

    states = controller.get_all_states()

    test_osc_cart_pose = [0.01, 0.0, 0.0, 0.0, 0.0, 0.0]
    controller.send_command('right_arm', ArmControlMode.OSC_CARTESIAN_POSE, np.array(test_osc_cart_pose), gripper_close=True)

    last_print_time = 0
    
    try:
        while True:
            current_time = time.time()
            
            # 每秒打印一次
            if current_time - last_print_time >= 1.0:
                states = controller.get_all_states()
                print_multi_arm_state(states)
                last_print_time = current_time
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        signal_handler(None, None)