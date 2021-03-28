from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='rosbridge_server',
            executable='rosbridge_websocket',
        ),
        Node(
            package='irradroom_python',
            executable='distance_measurement',
        ),
        Node(
            package='irradroom_python',
            executable='source_position',
        ),
        Node(
            package='irradroom_python',
            executable='door',
        ),
        Node(
            package='irradroom_python',
            executable='i2c_devices',
        ),
        Node(
            package='irradroom_python',
            executable='controller',
        ),
        Node(
            executable='python3 /root/dev_ws/IRRADROOM01/web/web.py',
        )
        ])



#
# import launch
# import launch.actions
# import launch.substitutions
# import launch_ros.actions
#
#
# def generate_launch_description():
#     return launch.LaunchDescription([
#
#         launch.actions.DeclareLaunchArgument(
#             'Launch',
#             default_value=[launch.substitutions.EnvironmentVariable('USER'), '_'],
#             description='Prefix for node names'),
#
#         launch_ros.actions.Node(
#             package='irradroom_python', executable='distance_measurement', output='screen'
#         ),
#     ])
