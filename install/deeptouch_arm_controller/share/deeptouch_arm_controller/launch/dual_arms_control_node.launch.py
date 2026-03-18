from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='deeptouch_arm_controller',
            executable='arm_controller_node',
            name='left_arm_controller_node',
            output='screen',
            parameters=[{
                'ip': "192.168.0.18",
                'port': 8080,
                'initial_joints': [16.737,52.108,29.185,83.404,18.195,90.774,87.215],
                'teleop_topic': "/teleoperation/left_cmd",
                'movej_vel': 15.0,
                "tool_frame": "gripper",
                "gripper_force": 350
            }]
        ),
        Node(
            package='deeptouch_arm_controller',
            executable='arm_controller_node',
            name='right_arm_controller_node',
            output='screen',
            parameters=[{
                'ip': "192.168.0.19",
                'port': 8080,
                'initial_joints': [5.875,-72.779,93.664,84.180,11.549,94.480,47.923],
                'teleop_topic': "/teleoperation/right_cmd",
                'movej_vel': 15.0,
                "tool_frame": "gripper",
                "gripper_force": 350
            }]
        )
    ])