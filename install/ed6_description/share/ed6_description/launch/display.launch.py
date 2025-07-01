import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_name = 'ed6_description'
    # 【修改點】指向RViz專用的xacro文件
    xacro_file_name = 'ed6_robot.rviz.xacro' 

    pkg_share_path = get_package_share_directory(pkg_name)
    xacro_file_path = os.path.join(pkg_share_path, 'urdf', xacro_file_name)
    
    robot_description_config = xacro.process_file(xacro_file_path).toxml()
    robot_description_param = {'robot_description': robot_description_config}

    # RViz可視化所需的節點
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description_param]
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
    )
    
    rviz_config_file = os.path.join(pkg_share_path, 'config', 'display.rviz')
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node,
    ])
