from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, TimerAction
from launch.conditions import IfCondition
from launch.substitutions import (
    Command,
    LaunchConfiguration,
    PathJoinSubstitution,
    FindExecutable
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    use_gui = LaunchConfiguration('gui')

    declare_gui = DeclareLaunchArgument(
        'gui',
        default_value='false',
        description='Start Gazebo GUI'
    )

    # ---------------- Paths ----------------
    urdf_file = PathJoinSubstitution([
        FindPackageShare('mobile_robot_description'),
        'urdf',
        'mobile_robot.urdf.xacro'
    ])

    world_file = PathJoinSubstitution([
        FindPackageShare('mobile_robot_description'),
        'worlds',
        'edges_academy.world'
    ])

    rviz_config = PathJoinSubstitution([
        FindPackageShare('mobile_robot_description'),
        'rviz',
        'mobile_robot.rviz'
    ])

    # ---------------- Robot Description ----------------
    robot_description = ParameterValue(
        Command([
            FindExecutable(name='xacro'),
            ' ',
            urdf_file
        ]),
        value_type=str
    )

    # ---------------- Nodes ----------------
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }],
        output='screen'
    )

    gzserver = ExecuteProcess(
        cmd=[
            FindExecutable(name='gzserver'),
            '--verbose',
            '-s', 'libgazebo_ros_init.so',
            '-s', 'libgazebo_ros_factory.so',
            world_file
        ],
        output='screen'
    )

    gzclient = ExecuteProcess(
        cmd=[FindExecutable(name='gzclient')],
        condition=IfCondition(use_gui),
        output='screen'
    )

    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'mobile_robot'
        ],
        output='screen'
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
        output='screen'
    )

    # ---------------- Turtle Bridge Node ----------------
    turtle_bridge_node = Node(
        package='gazebo_turtle_bridge_pkg',  # <-- your bridge package name
        executable='turtle_bridge_node',     # <-- Python node entry point
        name='bridge',
        output='screen',
        parameters=[
            {'linear_scale': 2.0},
            {'angular_scale': 2.0},
            {'enable_bridge': True}
        ]
    )

    # ---------------- Turtlesim Node ----------------
    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim',
        output='screen'
    )

    
    # ---------------- Launch Description ----------------
    return LaunchDescription([
        declare_gui,
        robot_state_publisher,
        gzserver,
        spawn_entity,
        rviz,
        turtlesim_node,
        turtle_bridge_node,          # <-- Added turtle bridge
        TimerAction(period=5.0, actions=[gzclient])
    ])
