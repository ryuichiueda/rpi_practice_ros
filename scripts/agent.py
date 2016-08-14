#!/usr/bin/env python
# vim:fileencoding=utf-8
import rospy,time,math
from std_msgs.msg import Int16MultiArray

def getrange(message):
    for i in range(4):
        ranges[i] = message.data[i]

if __name__ == '__main__':
    ranges = [0,0,0,0]
    pubdata = Int16MultiArray()
    pubdata.data = [0,0]

    rospy.init_node('agent')
    sub = rospy.Subscriber('lightsensors', Int16MultiArray, getrange)
    pub = rospy.Publisher('motor_raw', Int16MultiArray, queue_size=1)

    time.sleep(1)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        front_range = ranges[0] + ranges[3]
        target = 1500
        delta = target - front_range
        k = 0.3
        p_freq = delta * k
        cur_freq = pubdata.data[0]

        diff_limit = 20
        if math.fabs(p_freq) > math.fabs(cur_freq) + diff_limit:
            if p_freq < 0: p_freq -= diff_limit
            if p_freq > 0: p_freq += diff_limit

        pubdata.data = [p_freq,p_freq]

        pub.publish(pubdata)
        rate.sleep()
