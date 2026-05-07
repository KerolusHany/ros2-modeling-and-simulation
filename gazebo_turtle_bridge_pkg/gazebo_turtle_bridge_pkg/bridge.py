#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

class TurtleBridge(Node):
    def __init__(self):
        super().__init__('turtle_bridge_node')
        self.linear_scale = 1.0
        self.angular_scale = 1.0
        self.enable_bridge = True

        # Subscribe to odometry instead of /cmd_vel
        self.sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

    def odom_callback(self, msg):
        if not self.enable_bridge:
            return
        twist = Twist()
        twist.linear.x = msg.twist.twist.linear.x * self.linear_scale
        twist.angular.z = msg.twist.twist.angular.z * self.angular_scale
        self.pub.publish(twist)



def main(args=None):
    rclpy.init(args=args)
    node = TurtleBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
