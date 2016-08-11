#!/usr/bin/env python
# vim:fileencoding=utf-8
import rospy

# 型を定義したクラスを読み込み
from std_msgs.msg import Int16MultiArray

# ノードとして初期化
rospy.init_node('lightsensors')

# センサデータのパブリッシャーの準備
pub = rospy.Publisher('lightsensors', Int16MultiArray, queue_size=1)

# 送信データのインスタンスを作る
pubdata = Int16MultiArray()

# 読み込みを10Hzにする（遅れることアリ）
rate = rospy.Rate(10)

while not rospy.is_shutdown():
    #データをデバイスファイルから読み込む
    with open('/dev/rtlightsensor0','r') as f:
            data = f.readline().split()

    #データが左右逆になっているので逆に
    data.reverse()
    #整数型に直す
    pubdata.data = [ int(e) for e in data ]
    #パブリッシュ
    pub.publish(pubdata)
    #10Hzを保つためスリープ
    rate.sleep()
