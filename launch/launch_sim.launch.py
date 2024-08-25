import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():
    # Define the package name
    package_name = 'chunkbot_h'

    # Include the Robot State Publisher to publish the robot state
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name), 'launch', 'rsp.launch.py'
        )]),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Gazebo (now often referred to as GZ) launch description using ros_gz_sim
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    )

    # Spawn Entity in Gazebo using ros_gz_sim's create tool
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
        arguments=['-entity', 'chunkbot_h',
            '-topic', 'robot_description'],
        output='screen')

    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity
    ])