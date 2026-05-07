from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction, ExecuteProcess
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution, FindExecutable
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():

    use_gui = LaunchConfiguration('gui')

    declare_gui = DeclareLaunchArgument(
        'gui',
        default_value='true',
        description='Start GZ Sim GUI'
    )

    # Paths
    urdf_file = PathJoinSubstitution([
        FindPackageShare('mobile_robot_description'),
        'urdf',
        'mobile_robot_gzsim.urdf.xacro'
    ])

    world_file = PathJoinSubstitution([
        FindPackageShare('mobile_robot_description'),
        'worlds',
        'edges_academy.sdf'  # Use SDF world
    ])

    rviz_config = PathJoinSubstitution([
        FindPackageShare('mobile_robot_description'),
        'rviz',
        'mobile_robot.rviz'
    ])

    # Robot Description
    robot_description = ParameterValue(
        Command([
            FindExecutable(name='xacro'),
            ' ',
            urdf_file
        ]),
        value_type=str
    )

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }],
        output='screen'
    )

    # GZ Sim server
    gzserver = ExecuteProcess(
        cmd=[
            FindExecutable(name='ign'), 'gazebo',
            '--verbose',
            world_file,
            '-s', 'libignition-gazebo-ros-system.so'
        ],
        output='screen'
    )

    # GZ Sim client (GUI)
    gzclient = ExecuteProcess(
        cmd=[
            FindExecutable(name='ign'), 'gui',
            '--verbose'
        ],
        condition=IfCondition(use_gui),
        output='screen'
    )

    # Spawn Robot
    spawn_entity = Node(
        package='ros_ign_gazebo',
        executable='create',
        arguments=[
            '-name', 'mobile_robot',
            '-topic', 'robot_description'
        ],
        output='screen'
    )

    # RViz
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
        output='screen'
    )

    return LaunchDescription([
        declare_gui,
        robot_state_publisher,
        gzserver,
        spawn_entity,
        rviz,
        TimerAction(period=5.0, actions=[gzclient])
    ])