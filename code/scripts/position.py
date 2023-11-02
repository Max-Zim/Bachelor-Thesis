#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped

class PoseLogger:
    def __init__(self):
        # Initialize the ROS node
        rospy.init_node('pose_logger')

        # The time the first message is received
        self.first_received_time = None

        # Subscribe to the amcl_pose topic
        self.subscriber = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.callback)

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

        # Use print instead of rospy.loginfo
        print(f"Elapsed Time: {elapsed_time:.2f} seconds | Position: x={x:.2f}, y={y:.2f}")

    def run(self):
        # Keep the script running
        rospy.spin()

if __name__ == '__main__':
    pose_logger = PoseLogger()
    pose_logger.run()