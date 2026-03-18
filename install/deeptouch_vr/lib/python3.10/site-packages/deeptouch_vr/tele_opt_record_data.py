#!/usr/bin/env python3
"""
Main script to record robot data with RealSense cameras - Multi-arm version

Copyright (c) 2025 DeepTouch - 瞬恒智能科技（北京）有限公司
Author: max
All rights reserved.
"""

import argparse
import signal
import sys
import time
from pathlib import Path

import rclpy

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from record.data_record import DataRecorder


class RecordingManager:
    """Manager for the recording process - Multi-arm version"""
    
    def __init__(self, config_path: str):
        self.recorder = DataRecorder(config_path)
        self.running = True
        
        # Register signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        """Handle shutdown signals"""
        print("\n" + "=" * 60)
        print("Shutdown signal received!")
        print("Saving data and exiting...")
        print("=" * 60)
        
        self.running = False
        
        # Finalize dataset
        # self.recorder.finalize_dataset()
        
        # Shutdown recorder
        self.recorder.shutdown()
        
        # Shutdown ROS
        rclpy.shutdown()
        
        sys.exit(0)
    
    def run(self):
        """Main run loop"""
        print("=" * 60)
        print("Multi-Arm Robot Data Recorder for LeRobot 3.0")
        print("=" * 60)
        print("Dual-Arm Teleoperation Interface Active")
        print("-" * 60)
        print("Controls via ROS2 TeleOptCmd messages on topics:")
        
        # Show configured topics
        ros_config = self.recorder.config.get('teleoperation', {}).get('tele_opt_topic', {})
        left_topic = ros_config.get('left_teleopt_topic', '/teleoperation/left_cmd')
        right_topic = ros_config.get('right_teleopt_topic', '/teleoperation/right_cmd')
        
        print(f"  Left Arm:  {left_topic}")
        print(f"  Right Arm: {right_topic}")
        print("")
        print("Message fields (for each arm):")
        print("  - is_start_record: true to start, false to stop")
        print("  - is_discard_record: true to discard current episode")
        print("  - is_follow: true to control robot")
        print("  - hand_pose: target pose for robot")
        print("  - gripper_cmd: gripper control (true=close, false=open)")
        print("  - scale: scaling factor for movements")
        print("")
        print("Configured Systems:")
        print(f"  Robot Arms: {list(self.recorder.robot_controller.robot_configs.keys())}")
        print(f"  Cameras: {list(self.recorder.camera_manager.camera_configs.keys())}")
        print("")
        print("Press Ctrl+C to exit and finalize dataset")
        print("=" * 60)
        print("Waiting for commands...")
        print("")
        
        # Main loop
        try:
            while self.running:
                time.sleep(1.0)
                
                # Print status periodically
                if hasattr(self, '_last_status_time'):
                    if time.time() - self._last_status_time > 5.0:
                        # self._print_status()
                        self._last_status_time = time.time()
                else:
                    self._last_status_time = time.time()
                
        except KeyboardInterrupt:
            pass

    
    def _print_status(self):
        """Print current recording status"""
        if self.recorder.is_recording:
            print(f"📹 Recording: Episode {self.recorder.episode_counter}, "
                  f"Frame {self.recorder.current_frame_index}")
            
            # Show arm connection status
            connected = list(self.recorder.robot_controller.connected_arms)
            if not connected:
                print("   ⚠️  No arms connected")
        else:
            print(f"⏸️  Idle: {self.recorder.episode_counter} episodes recorded")


def main():
    parser = argparse.ArgumentParser(
        description='Record multi-arm robot data with RealSense cameras'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='/workspace/deeptouch/src/deeptouch_vr/deeptouch_vr/record/config/recording_config.yaml',  # 默认值
        help='Path to configuration file (default: config/recording_config.yaml)',
    )
    
    args = parser.parse_args()
    
    # Check if config file exists
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"❌ Configuration file not found: {config_path}")
        print("Please ensure recording_config.yaml exists in the current directory")
        sys.exit(1)
    
    # Initialize ROS2
    rclpy.init()
    
    # Create and run recorder
    manager = RecordingManager(args.config)
    manager.run()


if __name__ == "__main__":
    main()