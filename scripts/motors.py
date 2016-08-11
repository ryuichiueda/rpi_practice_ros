#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16MultiArray

def callback(message):
    with open('/dev/rtmotor_raw_l0','w') as lm:
        with open('/dev/rtmotor_raw_r0','w') as rm:
            print >> lm, str(message.data[0])
            print >> rm, str(message.data[1])

if __name__ == '__main__':
    rospy.init_node('motor')
    sub = rospy.Subscriber('motor_raw', Int16MultiArray, callback)
    rospy.spin()
