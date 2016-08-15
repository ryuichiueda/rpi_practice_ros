#!/usr/bin/env python
# vim:fileencoding=utf-8
import rospy,time,math,sys
from std_msgs.msg import Int16MultiArray
from rpi_ros_practice.msg import MotorFreqs
from rpi_ros_practice.srv import SwitchMotors

def getrange(message):
    for i in range(4):
        ranges[i] = message.data[i]

def switch_motors(onoff):
    rospy.wait_for_service('/practice/switch_motors')
    try:
        p = rospy.ServiceProxy('/practice/switch_motors', SwitchMotors)
        res = p(onoff)
        return res.result
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
        sys.exit(1)
    else:
        return res.result

if __name__ == '__main__':
    ranges = [0,0,0,0]
    pubdata = MotorFreqs()
    pubdata.left = 0
    pubdata.right = 0

    rospy.init_node('agent')
    sub = rospy.Subscriber('lightsensors', Int16MultiArray, getrange)
    pub = rospy.Publisher('motor_raw', MotorFreqs, queue_size=1)

    switch_motors("ON")
    time.sleep(1)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        front_range = ranges[0] + ranges[3]
        target = 1500
        delta = target - front_range
        k = 0.3
        p_freq = delta * k
        cur_freq = pubdata.right

        diff_limit = 20
        if math.fabs(p_freq) > math.fabs(cur_freq) + diff_limit:
            if p_freq < 0: p_freq -= diff_limit
            if p_freq > 0: p_freq += diff_limit

        pubdata.left = p_freq
        pubdata.right = p_freq

        pub.publish(pubdata)
        rate.sleep()
