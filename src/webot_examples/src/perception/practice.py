#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import rospy, math
import numpy as np
from std_msgs.msg import Int32MultiArray,String
from sensor_msgs.msg import LaserScan

class Detect_Obstacle():
    
    def __init__(self):
        rospy.loginfo("Lidar Receiver Object is Created")
        rospy.Subscriber("scan", LaserScan, self.detect_obstacle)
        self.obstacle_pub = rospy.Publisher("Obstacle_mission", String, queue_size= 1)

    # def __init__(self):
    #     # self.lidar = lidar
    #     self.lidar = None
    #     self.cnt = 0

    def filtering(self, x):
        return x > 0.15 and x < 3.0

    def filtering_zero(self, x):
        return x > 0

    def filter_obstacle(self, x):
        return x > 0.0 and x < 2.0

    def detect_obstacle(self,_data):   
        self.lidar = _data.ranges   
        self.cnt = 0    
        left = [0] * 8
        right = [0] * 8
        center = [0] * 8

        for j in range(8):
            left_temp = list(filter(self.filtering, self.lidar[100:325]))
            right_temp = list(filter(self.filtering, self.lidar[-325:-100]))
            center_temp_first = list(filter(self.filtering, self.lidar[:50]))
            center_temp_last = list(filter(self.filtering, self.lidar[-50:]))
            center_temp = center_temp_first + center_temp_last
            print("len center_temp", len(center_temp))
            
            
                
            if len(left_temp) != 0:
                if 0.1 < round(sum(left_temp)/len(left_temp), 2) < 1.5:
                    left[j] =  round(sum(left_temp)/len(left_temp), 2)
            if len(right_temp) != 0:
                if 0.1 < round(sum(right_temp)/len(right_temp), 2) < 1.5:
                    right[j] = round(sum(right_temp)/len(right_temp), 2)
            if len(center_temp) != 0:
                if 0.1 < round(sum(center_temp)/len(center_temp),2) < 1.0:
                    center[j] = round(sum(center_temp)/len(center_temp), 2)

        left = list(filter(self.filtering_zero, left))
        right = list(filter(self.filtering_zero, right))
        center = list(filter(self.filtering_zero, center))
        # print("left: ", left)
        # print("right: ", right)
        # print("center: ", center)

        if len(right) == 0:
            right = 0
        else:
            right = sum(right) / len(right)

        if len(left) == 0:
            left = 0
        else:
            left = sum(left) / len(left)
            
        if len(center) == 0:
            center = 0
        else:
            center = sum(center) / len(center)
            rospy.loginfo("center")    
            self.obstacle_pub.publish("center")
        

        print("left: ", left)
        print("right: ", right)
        print("center: ", center)
        # print("center: ", center)

        if right > left:
            rospy.loginfo("left")
            self.obstacle_pub.publish("left")
        elif left > right:
            rospy.loginfo("right")
            self.obstacle_pub.publish("right")
        else:
            rospy.loginfo("none")
            self.obstacle_pub.publish("none")

            
            
        
        
        # self.obstacle_pub.publish("left")
        # self.obstacle_pub.publish("right")
        # self.obstacle_pub.publish("center")
            


def run():
    rospy.init_node("lidar_example")
    new_class = Detect_Obstacle()
    rospy.spin()
    
if __name__ == '__main__':
    run()