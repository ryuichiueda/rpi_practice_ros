#include "ros/ros.h"
#include "std_msgs/Int16MultiArray.h"
#include <cmath>

int ranges[4] = {0,0,0,0};

void sensorUpdate(const std_msgs::Int16MultiArray::ConstPtr& msg)
{
	for(int i=0;i<4;i++)
		ranges[i] = msg->data[i];
}

int main(int argc, char **argv)
{
	std_msgs::Int16MultiArray putdata;
	putdata.data.push_back(0);
	putdata.data.push_back(0);

	ros::init(argc,argv,"agent");
	ros::NodeHandle n;

	ros::Subscriber sensor = n.subscribe("lightsensors", 3, sensorUpdate);
	ros::Publisher motor = n.advertise<std_msgs::Int16MultiArray>("motor_raw", 1);

	sleep(2);

	ros::Rate loop_rate(10);	
	while(ros::ok()){
		int front_range = ranges[0] + ranges[3];
		int target = 1500;
		int delta = target - front_range;
		double k = 0.3;
		double p_freq = delta * k;
		int cur_freq = putdata.data[0];

		int diff_limit = 20;
		if(fabs(p_freq) > fabs(cur_freq) + diff_limit){
			if(p_freq < 0)
				p_freq -= diff_limit;
			else
				p_freq += diff_limit;
		}

		putdata.data[0] = (int)p_freq;
		putdata.data[1] = (int)p_freq;
		motor.publish(putdata);

		ros::spinOnce();
		loop_rate.sleep();
	}
        return 0;
}
