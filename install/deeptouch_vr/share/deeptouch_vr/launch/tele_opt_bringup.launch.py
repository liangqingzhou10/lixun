# launch/tele_opt_bringup.launch.py
from launch import LaunchDescription
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        ExecuteProcess(cmd=['python3', '/workspace/deeptouch/src/deeptouch_vr/deeptouch_vr/tele_opt_cmd_publish.py'], output='screen'),
        ExecuteProcess(cmd=['python3', '/workspace/deeptouch/src/deeptouch_vr/deeptouch_vr/tele_opt_device_publish.py'], output='screen'),
        # ExecuteProcess(cmd=['python3', '/workspace/deeptouch/src/deeptouch_vr/launch/tele_opt_record_data.py'], output='screen'),
    ])