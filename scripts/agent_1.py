#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16MultiArray

def getrange(message):
    for i in range(4):
        ranges[i] = message.data[i]

if __name__ == '__main__':
    ranges = [0,0,0,0]
    rospy.init_node('motor')
    sub = rospy.Subscriber('lightsensors', Int16MultiArray, getrange)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        print ranges
        rate.sleep()
