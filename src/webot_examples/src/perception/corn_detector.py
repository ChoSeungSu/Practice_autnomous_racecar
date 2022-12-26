#!/usr/bin/env python 
#-*- coding: utf-8 -*- 

from pickletools import float8
import rospy # Ros에서 python을 활용할 수 있도록 한 부분 
#sensor_msgs/LaserScan 타입의 /scan 토픽을 받는 코드 작성
from sensor_msgs.msg import LaserScan # sensor_msgs/LaserScan 타입을 사용하기 위해 추가한 부분 
from std_msgs.msg import String , Float32 , Int32
import math 


class MovingAverage:

    def __init__(self, n):
        self.samples = n
        self.data = []
        self.weights = list(range(1, n + 1))

    def add_sample(self, new_sample):
        if len(self.data) < self.samples:
            self.data.append(new_sample)
        else:
            self.data = self.data[1:] + [new_sample]
            
    def get_sample_count(self):
        return len(self.data)
        
    def get_mm(self):
        return float(sum(self.data)) / len(self.data)

    def get_wmm(self):
        s = 0
        for i, x in enumerate(self.data):
            s += x * self.weights[i]
        return float(s) / sum(self.weights[:len(self.data)])

class LidarReceiver(): # LIDAR  데이터를 받아서 처리하는 클래스 생성
    def __init__(self): # 생성자 메서드
        rospy.loginfo("Corn Receiver Object is Created")
        rospy.Subscriber("/scan", LaserScan, self.lidar_callback) #  subscriber 생성자 필수 입력 매개변수 3가지 
        self.corn_pub = rospy.Publisher("corn_mission", Float32, queue_size= 3)
        self.avarge = MovingAverage(5)
        # 1. subscribe 하는 topic 이름 2. Topic message type , 동작 callback 함수 
        
    def lidar_callback(self, _data):

        theata_left_rad = []
        theata_right_rad = []
        
        min_left_idx = 0
        min_left_range = 1e9
        for i, distance in enumerate(_data.ranges[:325]):
            if distance < min_left_range:
                min_left_range = distance
                min_left_idx = i
                min_left_rad = (_data.angle_min + min_left_idx * _data.angle_increment)
                
        min_right_idx = 0
        min_right_range = 1e9
        for i, distance in enumerate(_data.ranges[-325:]):
            if distance < min_right_range:
                min_right_range = distance
                min_right_idx = i -243
                min_right_rad = (_data.angle_max + min_right_idx * _data.angle_increment)


        self.ref_rad = min_left_rad + min_right_rad
        # self.ref_rad = float(self.ref_rad)
        self.corn_pub.publish(self.ref_rad)
        rospy.loginfo("ref_rad = {}".format(self.ref_rad))

        
        
        

def run(): #실제 코드 동작 시 , 실행할 부분
    rospy.init_node("corn_example") # ros master에 노드 등록하는 함수
    new_class = LidarReceiver() #실제 동작을 담당하는 object
    rospy.spin() # ros node가 종료되지 않고, callback함수를 정상적으로 실행해주는 함수
    

if __name__ == '__main__': # 해당 python코드를 직접 실행할 때만 동작하도록 하는 함수
    run() # 실제 동작하는 코드 
