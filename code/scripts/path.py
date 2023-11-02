#!/usr/bin/env python

import rospy
from nav_msgs.msg import Path
import sys, select, termios, tty

path_count = 0
new_path_available = False
path_cache = None

def callback(data):
    global new_path_available, path_cache

    # Cache the path for logging when space is pressed
    path_cache = [(pose.pose.position.x, pose.pose.position.y) for pose in data.poses]
    new_path_available = True

def getKey():
    """Detect key presses in a non-blocking way."""
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
        if ord(key) == 3:  # ASCII value for Ctrl+C
            raise KeyboardInterrupt
    else:
        key = ''
    
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def listener():
    global path_count, new_path_available, path_cache

    # Initialize the node with a unique name
    rospy.init_node('path_logger_node', anonymous=True)

    # Subscribe to the given topic, specifying the message type and callback function
    rospy.Subscriber("/maxba/pa208756f27a7d/move_base/TebLocalPlannerROS/global_plan", Path, callback)

    print("Logging first path when received. Press space to log subsequent paths.")

    while not rospy.is_shutdown():
        if new_path_available and (path_count == 0 or getKey() == ' '):
            path_count += 1
            rospy.loginfo(f'Path #{path_count}: {path_cache}')
            new_path_available = False

if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)
    try:
        listener()
    except (rospy.ROSInterruptException, KeyboardInterrupt):
        pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
