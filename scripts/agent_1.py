#!/usr/bin/env python
# vim:fileencoding=utf-8
import rospy
from std_msgs.msg import Int16MultiArray

#センサの値を受け取った時のコールバック関数
def getrange(message):
    #非同期で動いている関係で一つずつコピー
    #（改善の余地あり）
    for i in range(4):
        ranges[i] = message.data[i]

if __name__ == '__main__':
    ranges = [0,0,0,0] #最新のセンサ値を入れるためのリスト
    rospy.init_node('motor')
    sub = rospy.Subscriber('lightsensors', Int16MultiArray, getrange)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        #rospy.loginfo等を使っても良いが、ここではprintで出力
        print ranges
        rate.sleep()
