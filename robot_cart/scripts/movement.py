#! /usr/bin/env python3
import threading
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sensor_msgs.msg
import random



class Vel_pub(Node):

    def __init__(self):
        super().__init__('imp_move_around')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.listener_callback)
        self.i = 0
        self.ri_side = []
        self.le_side = []

        self.subscription= self.create_subscription(sensor_msgs.msg.LaserScan, '/scan', self.listener_callback, qos_profile= 10)
        self.subscription


    def listener_callback(self, msg=[1]):
        if msg==[1]:
            return

        else:
            msg=msg
        self.ri_side = list(msg.ranges[0:50]).copy()
        self.le_side = list(msg.ranges[310:360]).copy()
        for i in range(len(self.le_side)):
            if not 0.0<self.le_side[i]<5.0: self.le_side[i] = 9999.9
            else: self.le_side[i] = float(self.le_side[i])
        for i in range(len(self.le_side)):
            if not 0.0<self.ri_side[i]<5.0: self.ri_side[i] = 9999.9
            else: self.ri_side[i] = float(self.ri_side[i])
        if min(self.ri_side) < 0.43:
            print('NOOOOOOOOOOOOOOOOO')
            imp_velocity = Twist()
            imp_velocity.linear.x = 0.0
            imp_velocity.angular.z = -0.5
            self.publisher_.publish(imp_velocity)
            self.get_logger().info(f"Publishing velocity: \n\t linear.x: {imp_velocity.linear.x}; \n\t angular.z: {imp_velocity.angular.z}")
            self.i+=1
        elif min(self.le_side) < 0.43:
            print('NOOOOOOOOOOOOOOOOO')
            imp_velocity = Twist()
            imp_velocity.linear.x = 0.0
            imp_velocity.angular.z = 0.5
            self.publisher_.publish(imp_velocity)
            self.get_logger().info(f"Publishing velocity: \n\t linear.x: {imp_velocity.linear.x}; \n\t angular.z: {imp_velocity.angular.z}")
            self.i+=1
        else:
            imp_velocity = Twist()
            imp_velocity.linear.x = 0.25
            imp_velocity.angular.z = 0.0
            self.publisher_.publish(imp_velocity)
            self.get_logger().info(f"Publishing velocity: \n\t linear.x: {imp_velocity.linear.x}; \n\t angular.z: {imp_velocity.angular.z}")
            self.i += 1
        self.ri_side = []
        self.le_side = []


def main(args=None):
    # initiate ROS2
    rclpy.init(args=args)

    # create an instance of the node
    velocity_pub = Vel_pub()


    # keep the node alive intil pressing CTRL+C
    rclpy.spin(velocity_pub)

    # destroy the node when it is not used anymore
    velocity_pub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

