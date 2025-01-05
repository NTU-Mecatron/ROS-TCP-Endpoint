#!/usr/bin/python3

import rospy
from pixhawk.msg import ManualControl
import time

last_published_time = time.time()

def callback(data):
    global last_published_time
    current_time = time.time()
    if (current_time - last_published_time) >= 0.05:
        pub.publish(data)
        last_published_time = current_time

if __name__ == '__main__':
    rospy.init_node('unity_manual_control_filtered_republisher', anonymous=True)
    pub = rospy.Publisher('/pixhawk/control/manual_control_filtered', ManualControl, queue_size=10)
    rospy.Subscriber('/pixhawk/control/manual_control_filtered_unity', ManualControl, callback)
    rospy.spin()