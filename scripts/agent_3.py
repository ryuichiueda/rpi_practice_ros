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
        #前向きのセンサーの値を足す
        front_range = ranges[0] + ranges[3]
        #最終的にfront_rangeをどんな値にしたいかをtargetに設定
        target = 1500
        #目標との差を求める
        delta = target - front_range
        #ゲイン
        k = 0.3
        #差にゲインをかけて入力周波数を決める
        p_freq = delta * k
        cur_freq = pubdata.data[0]

        #急に周波数を増加すると脱調するので制限
        diff_limit = 20
        if math.fabs(p_freq) > math.fabs(cur_freq) + diff_limit:
            if p_freq < 0:  p_freq -= diff_limit
            else:           p_freq += diff_limit

        #出力
        pubdata.data = [p_freq,p_freq]
        pub.publish(pubdata)
        rate.sleep()
