from ament_index_python.packages import get_package_share_directory

import os

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.substitutions import PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_arm02 = get_package_share_directory(
        'arm02')
    
    gui_config_path = os.path.join(pkg_arm02, 'config/arm02.config')
    
    pkg_ros_gz_sim = get_package_share_directory(
        'ros_gz_sim')

    gz_sim_launch = PathJoinSubstitution(
        [pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py'])

    gz_resource_path = SetEnvironmentVariable(name='GZ_SIM_RESOURCE_PATH',
                                               value=[os.path.join(
                                                      pkg_arm02,
                                                      'worlds')])
    
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([gz_sim_launch]),
        launch_arguments=[
            ('gz_args', ['-r --gui-config ' + gui_config_path, ' arm02.sdf'])
        ]
    )

    bridge = Node(
    package='ros_gz_bridge',
    executable='parameter_bridge',
    arguments=['/model/vehicle_blue/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
               '/lidar@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan'],
    remappings=[('/model/vehicle_blue/cmd_vel', '/cmd_vel'),
                ('/lidar', '/laser_scan')],
    output='screen'
    )

    ld = LaunchDescription()
    ld.add_action(gz_resource_path)
    ld.add_action(gz_sim)
    ld.add_action(bridge)
    return ld
