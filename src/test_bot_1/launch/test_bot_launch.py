import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    
    # specify the name of the package and path to xacro file
    pkg_name = 'test_bot_1'
    test_bot_path = 'urdf/test_bot.urdf.xacro'

    # use xacro to process the file
    xacro_file = os.path.join(get_package_share_directory(pkg_name),test_bot_path)
    robot_description_xml = xacro.process_file(xacro_file).toxml()

    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    gz_launch_path = PathJoinSubstitution([pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py'])
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gz_launch_path),
            launch_arguments = {
                'on_exit_shutdown': 'True'
            }.items(),
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description_xml}]
        ),
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[],
            remappings=[],
            output='screen'
        ),
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-topic', 'robot_description',
                       '-name', 'test_bot_1'],
            output='screen'
        )
        ])
