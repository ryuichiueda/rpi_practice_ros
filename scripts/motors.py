#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16MultiArray

def callback(message):
    with open('/dev/rtmotor_raw_l0','w') as lm:
        with open('/dev/rtmotor_raw_r0','w') as rm:
            print >> lm, str(message.data[0])
            print >> rm, str(message.data[1])

def stop_motor():
    for s in [ "_raw_l0" , "_raw_r0", "en0" ]:
        with open('/dev/rtmotor' + s,'w') as f:
            print >> f, "0"

if __name__ == '__main__':
    with open('/dev/rtmotoren0','w') as f:
        print >> f, "1"

    rospy.init_node('motor')
    sub = rospy.Subscriber('motor_raw', Int16MultiArray, callback)
    rospy.on_shutdown(stop_motor)
    rospy.spin()
