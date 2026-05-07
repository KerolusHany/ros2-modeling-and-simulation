# Mobile Robot ROS2 Project

A ROS2-based mobile robot simulation project featuring Gazebo integration, TurtleSim bridging, and comprehensive robot modeling with URDF/Xacro descriptions.

---

## 📋 Project Overview

This project implements a complete mobile robot system with the following capabilities:

- **Robot Simulation**: Full kinematic and dynamic mobile robot model in Gazebo
- **Robot Bridging**: Bridge between Gazebo robot and TurtleSim for velocity mirroring
- **Visualization**: RViz integration for real-time visualization and monitoring
- **Modular Architecture**: Organized into separate ROS2 packages for maintainability

---

## 📦 Project Structure

### Package: `mobile_robot_description`
**Location**: `mobile_robot_description/`

Contains all robot configuration and description files:

#### URDF/Xacro Files:
- **`urdf/mobile_robot.xacro`**: Main robot description with detailed parameters
  - Base dimensions: 0.7m (length) × 0.4m (width) × 0.2m (height)
  - Wheel radius: 0.1m
  - Wheel length: 0.08m
  - Includes macros for inertia calculations (box, cylinder, sphere)
  - Defines kinematics with 3 wheels: left, right, and caster wheel
  - Collision geometry and mass properties included

- **`urdf/mobile_robot_gzsim.urdf.xacro`**: Gazebo-specific URDF configuration
  - Simplified robot structure for simulation
  - Base link, caster wheel, left wheel, and right wheel definitions
  - Material definitions (black base, blue wheels, red caster)

- **`urdf/mobile_robot_gazebo.xacro`**: Gazebo plugin configurations
- **`urdf/material.xacro`**: Material definitions for visualization

#### Simulation & Visualization:
- **`worlds/edges_academy.sdf`**: Gazebo world file defining the simulation environment
- **`rviz/mobile_robot.rviz`**: RViz configuration for robot visualization

---

### Package: `mobile_robot_bringup`
**Location**: `mobile_robot_bringup/`

Launch files and initialization configuration for the robot system.

#### Launch Files:
- **`launch/mobile_robot_gzsim.launch.py`**: Main launch file for Gazebo simulation
  - Launches Gazebo server with physics simulation
  - Starts Gazebo GUI (optional, controlled via `gui:=true/false` argument)
  - Publishes robot description from xacro file
  - Spawns the robot entity in Gazebo
  - Starts Robot State Publisher for TF broadcasting
  - Launches RViz for visualization

- **`launch/mobile_robot.launch.py`**: Alternative launch configuration

#### Features:
- Uses ROS2 Ignition (formerly Gazebo) with ROS integration
- Robotics Operating System plugins for seamless ROS2 integration
- Configurable GUI launch option

---

### Package: `gazebo_turtle_bridge_pkg`
**Location**: `gazebo_turtle_bridge_pkg/`

Python package implementing a bridge between the Gazebo robot and TurtleSim.

#### Implementation:
- **`gazebo_turtle_bridge_pkg/bridge.py`**: Main bridge node implementation

#### Functionality:
- **Node Name**: `turtle_bridge_node`
- **Subscriptions**: 
  - Subscribes to `/odom` (Odometry messages from the mobile robot)
- **Publications**: 
  - Publishes velocity commands to `/turtle1/cmd_vel` (TurtleSim turtle velocity)
- **Features**:
  - Velocity scaling for linear and angular motion (default: 1.0)
  - Enable/disable switch for the bridge
  - Converts Gazebo odometry to TurtleSim velocity commands
  - Seamless integration between real robot simulation and TurtleSim visualization

#### Entry Point:
```
console_scripts:
  'turtle_bridge_node = gazebo_turtle_bridge_pkg.bridge:main'
```

#### Dependencies:
- `rclpy`: ROS2 Python client library
- `geometry_msgs`: Geometry message types (Twist)
- `nav_msgs`: Navigation message types (Odometry)
- `turtlesim`: TurtleSim package for turtle simulation

---

## 🚀 Installation & Setup

### Prerequisites
- ROS2 (Humble or latest version)
- Python 3.8+
- Gazebo (Harmonic recommended)
- RViz2
- TurtleSim

### Dependencies Installation
```bash
# Navigate to workspace
cd ~/mobile_robot_ws

# Install dependencies
rosdep install --from-paths src --ignore-src -r -y

# Install Python dependencies
pip install setuptools
```

### Building the Project
```bash
# From workspace root
colcon build

# Source the setup script
source install/setup.bash
```

---

## 🏃 Running the Project

### 1. Launch the Main Robot Simulation
```bash
ros2 launch mobile_robot_bringup mobile_robot_gzsim.launch.py
```

**Optional Arguments:**
- Disable GUI: `ros2 launch mobile_robot_bringup mobile_robot_gzsim.launch.py gui:=false`

This will:
- Start Gazebo simulation environment
- Launch Gazebo server and GUI
- Spawn the mobile robot in the world
- Start Robot State Publisher for TF broadcasting
- Open RViz with robot visualization

### 2. Start the TurtleSim Bridge
In a new terminal:
```bash
# Source the workspace
source install/setup.bash

# Run the bridge node
ros2 run gazebo_turtle_bridge_pkg turtle_bridge_node
```

### 3. Start TurtleSim (Optional)
In another terminal:
```bash
ros2 run turtlesim turtlesim_node
```

---

## 📡 ROS2 Topics & Communication

### Topic Mappings

| Source Topic | Bridge | Destination Topic | Message Type |
|---|---|---|---|
| `/odom` | Receives from | - | `nav_msgs/Odometry` |
| - | Publishes to | `/turtle1/cmd_vel` | `geometry_msgs/Twist` |

### Robot State
- **TF Transforms**: Published via `robot_state_publisher`
- **Odometry**: Published by Gazebo simulation
- **Base Footprint**: Reference frame for robot positioning

---

## 🔧 Configuration

### Velocity Scaling
Edit [gazebo_turtle_bridge_pkg/bridge.py](gazebo_turtle_bridge_pkg/gazebo_turtle_bridge_pkg/bridge.py):
```python
self.linear_scale = 1.0      # Adjust linear velocity scaling
self.angular_scale = 1.0     # Adjust angular velocity scaling
```

### Robot Dimensions
Edit [urdf/mobile_robot.xacro](mobile_robot_description/urdf/mobile_robot.xacro):
```xml
<xacro:property name="length"        value="0.7" />   <!-- Base length -->
<xacro:property name="width"         value="0.4" />   <!-- Base width -->
<xacro:property name="height"        value="0.2" />   <!-- Base height -->
<xacro:property name="wheel_radius"  value="0.1" />   <!-- Wheel radius -->
```

### RViz Configuration
Modify [rviz/mobile_robot.rviz](mobile_robot_description/rviz/mobile_robot.rviz) to customize visualization displays.

---

## 📊 Robot Specifications

### Physical Properties
- **Chassis Material**: Black box (mass: 2.0 kg)
- **Caster Wheel**: Sphere (mass: 0.5 kg, radius: 0.1m)
- **Drive Wheels**: Cylinders (mass: 0.5 kg each, radius: 0.1m, length: 0.08m)
- **Total Base Dimensions**: 0.7m × 0.4m × 0.2m

### Kinematic Chain
```
base_footprint
├── base_link (fixed joint)
│   ├── caster_wheel_link (fixed)
│   ├── continuous_link (continuous joint for left wheel)
│   └── continuous2_link (continuous joint for right wheel)
```

### Inertia Calculations
The robot includes proper moment of inertia calculations for:
- Box shapes (base chassis)
- Cylinder shapes (drive wheels)
- Sphere shapes (caster wheel)

---

## 🐛 Troubleshooting

### Gazebo Won't Launch
```bash
# Ensure Gazebo is properly installed
sudo apt update && sudo apt install ignition-harmonic

# Check for missing plugins
export IGN_GAZEBO_SYSTEM_PLUGIN_PATH=$IGN_GAZEBO_SYSTEM_PLUGIN_PATH:/usr/lib/x86_64-linux-gnu/ign-gazebo-6/plugins
```

### Bridge Node Not Receiving Odometry
- Verify Gazebo is running: `ros2 topic list | grep odom`
- Check topic namespace: `ros2 topic echo /odom`

### RViz Not Showing Robot
- Ensure `robot_state_publisher` is running
- Check TF tree: `ros2 run tf2_tools view_frames`

### TurtleSim Not Responding
- Verify TurtleSim is running: `ros2 node list`
- Check bridge is publishing: `ros2 topic echo /turtle1/cmd_vel`

---

## 📝 File Distribution

### By Package

**mobile_robot_description/**
- `package.xml` - Package metadata
- `urdf/` - 5 URDF/Xacro files
- `rviz/` - RViz configuration
- `worlds/` - Gazebo world definition

**mobile_robot_bringup/**
- `package.xml` - Package metadata
- `CMakeLists.txt` - Build configuration
- `launch/` - 2 launch files

**gazebo_turtle_bridge_pkg/**
- `package.xml` - Package metadata (Python package)
- `setup.py` - Python setup configuration
- `setup.cfg` - Setup configuration
- `gazebo_turtle_bridge_pkg/` - Python source
  - `__init__.py` - Package initialization
  - `bridge.py` - Main bridge implementation
- `resource/` - Package resources
- `test/` - Unit tests

---

## 🛠️ Development

### Adding New Features

#### To the Robot Model:
1. Edit relevant `.xacro` file in `urdf/`
2. Rebuild: `colcon build`
3. Test with: `ros2 launch mobile_robot_bringup mobile_robot_gzsim.launch.py`

#### To the Bridge:
1. Modify `gazebo_turtle_bridge_pkg/bridge.py`
2. Rebuild: `colcon build`
3. Run: `ros2 run gazebo_turtle_bridge_pkg turtle_bridge_node`

#### To Launch Configuration:
1. Edit `.launch.py` file
2. No rebuild needed, changes take effect immediately

### Testing
```bash
# Run package tests
colcon test

# Check Python code quality
flake8 gazebo_turtle_bridge_pkg/
```

---

## 📚 References

- [ROS2 Documentation](https://docs.ros.org/en/humble/)
- [URDF Tutorial](http://wiki.ros.org/urdf/Tutorials)
- [Gazebo-ROS Integration](https://github.com/gazebosim/ros_gz)
- [TurtleSim Package](https://index.ros.org/p/turtlesim/)

---

## 👤 Maintainer

**Kerolus Hany**  
`kerolushany8@gmail.com`

---

## 📄 License

Apache License 2.0

---

## 🎯 Summary

This project demonstrates:
- ✅ Complete robot modeling with URDF/Xacro
- ✅ Gazebo simulation integration
- ✅ ROS2 node communication
- ✅ Robot state publishing and TF management
- ✅ Multi-robot system coordination (Gazebo + TurtleSim)
- ✅ Launch file configuration
- ✅ Modular architecture best practices

Perfect for learning ROS2 robotics fundamentals and simulation concepts!
