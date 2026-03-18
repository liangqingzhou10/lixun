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

import threading
from typing import Optional, Callable, Dict
import logging

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose
from deeptouch_interface.msg import TeleOptCmd


class TeleOptSubscriber(Node):
    """ROS2 subscriber for teleoperation commands - Multi-arm version with recording state management"""
    
    def __init__(self, config: dict):
        super().__init__('teleopt_subscriber')
        
        self.config = config
        self.logger = logging.getLogger("TeleOptSubscriber")
        
        # Callback function for data recorder
        self.recorder_callback = None
        
        # Latest messages for each arm
        self.latest_msgs = {}
        self.msg_locks = {}
        
        # Recording state management (only monitor right hand record_state)
        self.current_recording_state = 'idle'
        self.prev_recording_state = 'idle'
        
        # Get teleopt topics configuration
        tele_opt_config = config.get('tele_opt_topic', {})
        
        # Create subscriptions for each arm
        self._arm_subscriptions = {}
        
        # Left arm subscription
        left_topic = tele_opt_config.get('left_teleopt_topic', '/teleoperation/left_cmd')
        self._arm_subscriptions['left'] = self.create_subscription(
            TeleOptCmd,
            left_topic,
            lambda msg: self._on_teleopt_cmd('left', msg),
            10
        )
        self._initialize_arm_state('left')
        
        # Right arm subscription  
        right_topic = tele_opt_config.get('right_teleopt_topic', '/teleoperation/right_cmd')
        self._arm_subscriptions['right'] = self.create_subscription(
            TeleOptCmd,
            right_topic,
            lambda msg: self._on_teleopt_cmd('right', msg),
            10
        )
        self._initialize_arm_state('right')
        
        # Start ROS2 spin in separate thread
        self.ros_thread = threading.Thread(target=self._ros_spin, daemon=True)
        self.ros_thread.start()
        
        self.logger.info(f"TeleOptSubscriber initialized for dual arms:")
        self.logger.info(f"  Left topic:  {left_topic}")
        self.logger.info(f"  Right topic: {right_topic}")
        self.logger.info(f"Recording states: 'idle', 'recording', 'stop_record', 'save'")

    def _initialize_arm_state(self, arm_name: str):
        """Initialize state for an arm"""
        self.latest_msgs[arm_name] = None
        self.msg_locks[arm_name] = threading.Lock()

    def register_callback(self, callback: Callable):
        """Register callback function for message processing"""
        self.recorder_callback = callback
        self.logger.info("Registered recorder callback")

    def _on_teleopt_cmd(self, arm_name: str, msg: TeleOptCmd):
        """Handle TeleOptCmd message for specific arm"""
        with self.msg_locks[arm_name]:
            self.latest_msgs[arm_name] = msg
            
            # 只从右手的消息中获取录制状态
            if arm_name == 'right':
                self.current_recording_state = msg.record_state
                self._process_recording_state_change()
            
    def _process_recording_state_change(self):  
        """  
        Process recording state changes and trigger appropriate, explicit actions.  
        This is the new, corrected logic.  
        """  
        if self.current_recording_state == self.prev_recording_state:  
            return  # No state change, do nothing  

        self.logger.info(f"📊 Recording state changed: {self.prev_recording_state} → {self.current_recording_state}")  

        if not self.recorder_callback:  
            self.logger.warning("Recorder callback is not registered. Cannot send commands.")  
            self.prev_recording_state = self.current_recording_state  
            return  

        # 1. 从任何状态进入 'recording' 状态，都意味着开始录制  
        if self.current_recording_state == 'recording':  
            self.logger.info("🎬 Start recording command issued.")  
            self.recorder_callback('start_recording', 'right', self.latest_msgs.get('right'))  

        # 2. 从 'recording' 状态进入 'stop_record' 状态  
        elif self.current_recording_state == 'stop_record' and self.prev_recording_state == 'recording':  
            self.logger.info("⏹️ Stop detected. Entering save/discard window. Waiting for next command...")  

        # 3. 从 'stop_record' 状态进入 'save' 状态   
        elif self.current_recording_state == 'save' and self.prev_recording_state == 'stop_record':  
            self.logger.info("💾 Save command confirmed. Sending 'stop_and_save_recording' event.")  
            self.recorder_callback('stop_and_save_recording', 'right', self.latest_msgs.get('right'))  
        
        # 4. 从 'recording' 或 'stop_record' 状态直接回到 'idle'  
        elif self.current_recording_state == 'idle' and self.prev_recording_state in ['recording', 'stop_record']:  
            if self.prev_recording_state == 'recording':  
                self.logger.info("❌ Recording cancelled during operation. Sending 'stop_and_discard_recording' event.")  
            else: # prev_recording_state == 'stop_record'  
                self.logger.info("🗑️ Discard confirmed (e.g., via timeout). Sending 'stop_and_discard_recording' event.")  
        
            self.recorder_callback('stop_and_discard_recording', 'right', self.latest_msgs.get('right'))  
        
        # 5. 处理从 'save' 状态回到 'idle' 的情况  
        elif self.current_recording_state == 'idle' and self.prev_recording_state == 'save':  
            self.logger.info("✅ Save process finished. Returning to idle state.")  
            # 不需要给 DataRecorder 发送指令，因为它已经在上一步处理完了  

        # Finally, update the previous state for the next cycle  
        self.prev_recording_state = self.current_recording_state  

    def _ros_spin(self):
        """ROS2 spin loop"""
        try:
            rclpy.spin(self)
        except Exception as e:
            self.logger.error(f"Error in ROS spin: {e}")

    def get_latest_msg(self, arm_name: str) -> Optional[TeleOptCmd]:
        """Get the latest received message for specific arm"""
        with self.msg_locks[arm_name]:
            return self.latest_msgs[arm_name]

    def get_all_latest_msgs(self) -> Dict[str, Optional[TeleOptCmd]]:
        """Get latest messages for all arms"""
        msgs = {}
        for arm_name in self.latest_msgs.keys():
            msgs[arm_name] = self.get_latest_msg(arm_name)
        return msgs

    def get_current_recording_state(self) -> str:
        """Get current recording state"""
        return self.current_recording_state

    def get_recording_state_info(self) -> Dict[str, str]:
        """Get detailed recording state information"""
        state_descriptions = {
            'idle': '待机状态 - 未在录制',
            'recording': '录制中 - 正在记录数据',
            'stop_record': '录制停止 - 等待保存或丢弃指令',
            'discard': '丢弃中 - 正在丢弃录制数据'
        }
        
        return {
            'current_state': self.current_recording_state,
            'previous_state': self.prev_recording_state,
            'description': state_descriptions.get(self.current_recording_state, '未知状态'),
            'is_recording_active': self.current_recording_state == 'recording'
        }

    def is_recording(self) -> bool:
        """Check if currently recording"""
        return self.current_recording_state == 'recording'

    def is_in_save_window(self) -> bool:
        """Check if in save/discard decision window"""
        return self.current_recording_state == 'stop_record'

    def shutdown(self):
        """Shutdown the ROS node"""
        self.logger.info("Shutting down TeleOptSubscriber...")
        
        # Final state notification
        if self.recorder_callback and self.current_recording_state != 'idle':
            self.logger.warning(f"Shutting down while in state: {self.current_recording_state}")
            self.recorder_callback('shutdown', 'system', None)
        
        self.destroy_node()
        if self.ros_thread.is_alive():
            self.ros_thread.join(timeout=2.0)
        
        self.logger.info("TeleOptSubscriber shutdown completed")


def main():
    """Test function for TeleOptSubscriber"""
    import time
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize ROS2
    rclpy.init()
    
    # Test configuration
    config = {
        'tele_opt_topic': {
            'left_teleopt_topic': '/teleoperation/left_cmd',
            'right_teleopt_topic': '/teleoperation/right_cmd'
        }
    }
    
    def test_callback(action, arm_name, msg):
        """Test callback function"""
        if action == 'update':
            if msg:
                print(f"📝 Update from {arm_name}: record_state={msg.record_state}, follow={msg.is_follow}, gripper={msg.gripper_cmd}")
        else:
            print(f"🎯 Action: {action} from {arm_name}")
            if msg:
                print(f"   Associated state: {msg.record_state}")
    
    try:
        # Create subscriber
        subscriber = TeleOptSubscriber(config)
        subscriber.register_callback(test_callback)
        
        print("TeleOptSubscriber test started. Listening for messages...")
        print("Expected recording state transitions (from tele_opt_cmd_publish.py):")
        print("  idle → recording → stop_record → idle (timeout/auto-save)")
        print("  idle → recording → idle (cancel)")
        print("  stop_record → recording (new recording)")  
        print("  stop_record → discard → idle")
        print("\nPress Ctrl+C to exit")
        
        # Monitor state changes
        last_state = 'idle'
        frame_count = 0
        
        while rclpy.ok():
            current_state = subscriber.get_current_recording_state()
            if current_state != last_state:
                state_info = subscriber.get_recording_state_info()
                print(f"\n📊 State Change: {last_state} → {current_state}")
                print(f"   Description: {state_info['description']}")
                print(f"   Is Recording: {state_info['is_recording_active']}")
                last_state = current_state
            
            # Show periodic activity
            frame_count += 1
            if frame_count % 100 == 0:  # Every 10 seconds at 10Hz
                all_msgs = subscriber.get_all_latest_msgs()
                active_arms = [name for name, msg in all_msgs.items() if msg is not None]
                if active_arms:
                    print(f"📡 Active arms: {', '.join(active_arms)} (State: {current_state})")
            
            time.sleep(0.1)  # 10Hz
            
    except KeyboardInterrupt:
        print("\nShutting down test...")
    finally:
        if 'subscriber' in locals():
            subscriber.shutdown()
        rclpy.shutdown()
        print("Test completed")


if __name__ == "__main__":
    main()