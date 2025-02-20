import os
import launch
import launch_ros.actions
import xacro
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    urdf_pkg_path = FindPackageShare("ur_description").find("ur_description")
    urdf_file_path = os.path.join(urdf_pkg_path, "urdf", "ur.urdf.xacro")

    # Generate URDF from Xacro
    robot_description = Command(["xacro ", urdf_file_path])

    # Launch arguments
    use_sim_time = LaunchConfiguration("use_sim_time", default="true")

    # Robot State Publisher
    robot_state_publisher = launch_ros.actions.Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description, "use_sim_time": use_sim_time}]
    )

    # Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("gazebo_ros"), "/launch/gazebo.launch.py"]
        ),
        launch_arguments={"use_sim_time": use_sim_time}.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument("use_sim_time", default_value="true", description="Use simulation time"),
        gazebo,
        robot_state_publisher
    ])
