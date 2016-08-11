#!/usr/bin/env python
# vim:fileencoding=utf-8
import rospy
from std_msgs.msg import Int16MultiArray

#モータへの指令値を他のノードから受け取った時のコールバック関数
def callback(message):
    #左右のデバイスファイルを開いて値を書き込む
    #左右で時間差が生じないように両方開いてから書き込んでいるが
    #凝りすぎかもしれない
    with open('/dev/rtmotor_raw_l0','w') as lm:
        with open('/dev/rtmotor_raw_r0','w') as rm:
            print >> lm, str(message.data[0])
            print >> rm, str(message.data[1])

#ノードが落ちる時に呼ばれる関数（このファイルの下から2行目参照のこと）
def stop_motor():
    #左右のモータの周波数を0にして、最後に電源OFF
    for s in [ "_raw_l0" , "_raw_r0", "en0" ]:
        with open('/dev/rtmotor' + s,'w') as f:
            print >> f, "0"

if __name__ == '__main__':
    #ノードが立ち上がった時に電源を自動で立ち上げる（手抜き）
    with open('/dev/rtmotoren0','w') as f:
        print >> f, "1"

    #ノードとして初期化
    rospy.init_node('motor')
    #サブスクライバを作る
    sub = rospy.Subscriber('motor_raw', Int16MultiArray, callback)
    #stop_motorが終了時に呼ばれるようにセット
    rospy.on_shutdown(stop_motor)
    #リッスンの無限ループに入る
    rospy.spin()
