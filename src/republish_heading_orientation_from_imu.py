#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32
from geometry_msgs.msg import QuaternionStamped
import tf

def imu_callback(data):
    # Extract orientation in quaternion
    orientation = data.orientation

    # Convert quaternion to Euler angles
    quaternion = (
        orientation.x,
        orientation.y,
        orientation.z,
        orientation.w
    )
    euler = tf.transformations.euler_from_quaternion(quaternion)
    
    # Extract yaw (heading) in radians and convert to degrees
    yaw = -euler[2]
    heading = yaw * 180.0 / 3.141592653589793

    # Create QuaternionStamped message
    orientation_stamped = QuaternionStamped()
    orientation_stamped.header.stamp = rospy.Time.now()
    orientation_stamped.header.frame_id = "imu_frame"  # Set the appropriate frame_id
    orientation_stamped.quaternion = orientation

    # Publish heading and orientation
    heading_pub.publish(heading)
    orientation_pub.publish(orientation_stamped)

if __name__ == '__main__':
    rospy.init_node('republish_heading_orientation_from_imu', anonymous=True)

    # Publishers
    heading_pub = rospy.Publisher('/pixhawk/vehicle_status/heading', Float32, queue_size=10)
    orientation_pub = rospy.Publisher('/pixhawk/vehicle_status/orientation', QuaternionStamped, queue_size=10)

    # Subscriber
    rospy.Subscriber('/sensor/imu', Imu, imu_callback)

    rospy.spin()