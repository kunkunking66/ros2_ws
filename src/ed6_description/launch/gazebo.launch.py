import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_name = 'ed6_description'
    # 【修改點】指向Gazebo專用的xacro文件
    xacro_file_name = 'ed6_robot.gazebo.xacro'

    pkg_share_path = get_package_share_directory(pkg_name)
    xacro_file_path = os.path.join(pkg_share_path, 'urdf', xacro_file_name)
    
    robot_description_config = xacro.process_file(xacro_file_path).toxml()
    robot_description_param = {'robot_description': robot_description_config}

    # Gazebo 啓動
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    )

    # 節點定義
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description_param]
    )
    
    spawn_entity_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'ed6_robot'],
        output='screen'
    )

    spawn_joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    spawn_ed6_arm_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["ed6_arm_controller", "--controller-manager", "/controller_manager"],
    )
    
    return LaunchDescription([
        gazebo,
        robot_state_publisher_node,
        spawn_entity_node,
        spawn_joint_state_broadcaster,
        spawn_ed6_arm_controller,
    ])
