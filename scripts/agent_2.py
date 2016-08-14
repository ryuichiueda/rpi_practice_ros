#!/usr/bin/env python
# vim:fileencoding=utf-8
import rospy
from std_msgs.msg import Int16MultiArray

def getrange(message):
    for i in range(4):
        ranges[i] = message.data[i]

if __name__ == '__main__':
    ranges = [0,0,0,0]
    pubdata = Int16MultiArray() #モータに値を投げるためのインスタンス
    pubdata.data = [1000,1000] #初期値（この例では変化させず）

    rospy.init_node('agent')
    sub = rospy.Subscriber('lightsensors', Int16MultiArray, getrange)
    pub = rospy.Publisher('motor_raw', Int16MultiArray, queue_size=1)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        print ranges
        pub.publish(pubdata) #何度も同じデータを投げているだけ
        rate.sleep()
