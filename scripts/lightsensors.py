#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16MultiArray

rospy.init_node('lightsensors')
pub = rospy.Publisher('lightsensors', Int16MultiArray, queue_size=1)
pubdata = Int16MultiArray()
rate = rospy.Rate(10)

while not rospy.is_shutdown():
    with open('/dev/rtlightsensor0','r') as f:
            data = f.readline().split()
    data.reverse()
    pubdata.data = [ int(e) for e in data ]
    pub.publish(pubdata)

    rate.sleep()
