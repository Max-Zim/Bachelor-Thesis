#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry

class OdometryLogger:
    def __init__(self):
        # Initialize the ROS node
        rospy.init_node('odometry_logger')

        # The time the first message is received
        self.first_received_time = None

        # Subscribe to the odom topic
        self.subscriber = rospy.Subscriber('/odom', Odometry, self.callback)

    def callback(self, msg):
        # Get the current time
        current_time = rospy.get_time()

        # If this is the first received message, set the first_received_time to the current time
        if self.first_received_time is None:
            self.first_received_time = current_time

        # Calculate the elapsed time since the first received message
        elapsed_time = current_time - self.first_received_time

        # Extract the x and y position from the pose
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        # Use print to output the information
        print(f"Elapsed Time: {elapsed_time:.2f} seconds | Position: x={x:.2f}, y={y:.2f}")

    def run(self):
        # Keep the script running
        rospy.spin()

if __name__ == '__main__':
    odometry_logger = OdometryLogger()
    odometry_logger.run()