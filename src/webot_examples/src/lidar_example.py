#!/usr/bin/env python 
#-*- coding: utf-8 -*- 

import rospy # Ros에서 python을 활용할 수 있도록 한 부분 
#sensor_msgs/LaserScan 타입의 /scan 토픽을 받는 코드 작성
from sensor_msgs.msg import LaserScan # sensor_msgs/LaserScan 타입을 사용하기 위해 추가한 부분 
from std_msgs.msg import String
import math 

class LidarReceiver(): # LIDAR  데이터를 받아서 처리하는 클래스 생성
    def __init__(self): # 생성자 메서드
        rospy.loginfo("Lidar Receiver Object is Created")
        rospy.Subscriber("scan", LaserScan, self.lidar_callback) #  subscriber 생성자 필수 입력 매개변수 3가지 
        self.warning_pub = rospy.Publisher("Lidar_warning", String, queue_size= 3)
        self.lidar_data = []
        # 1. subscribe 하는 topic 이름 2. Topic message type , 동작 callback 함수 
        
    def lidar_callback(self, _data): # 실제 LIDAR 데이터를 받고 동작하는 메서드
        # rospy.loginfo(_data)
        # rospy.loginfo(len(_data.ranges))
        rospy.loginfo("{} m".format(_data.ranges[-100:-90]))

        
        # 측정된 거리 값 중, 센서와 가장 까이에 있는 물체의 거리와 각도를 표시해주는 코드 (r, theata, x, y)
        # 해당 하드웨어에 종속되지 않는 범용적인 코드 작성
        # 실질적인 사용을 위해서는 (r,theata) --> (x,y)로 변경할 필요가 있음
        
        #1단계 --> ranges에 해당하는 각도를 구해옴--------------------------
        # theata_rad = []
        # for i in range(len(_data.ranges)):
        #     tmp_theata = _data.angle_min + i * _data.angle_increment
        #     if tmp_theata >= _data.angle_max:
        #         tmp_theata = _data.angle_max
        #     theata_rad.append(tmp_theata)
        # # rospy.loginfo(theata_rad)
        # #rospy.loginfo(len(_data.ranges))
        
        # #2단계 --> ranges 중 최소 거리 값을 찾기---------------------
        # min_idx = 0
        # min_range = 1e9
        # for i, distance in enumerate(_data.ranges):
        #     if distance < min_range:
        #         min_range = distance
        #         min_idx = i
        # #3단계 --> 거리값과 각도를 계산하여 x,y로 변환하기 ----------------
        # # 최소 거리값 : min_range  최소 거리에 해당하는 각도값 : theata_rad[min_idx]
        # # x = r cos(theata) y = r sin(theata) theata는 라디안
        # x = min_range * math.cos(theata_rad[min_idx])
        # y = min_range * math.sin(theata_rad[min_idx])  
           
        # #4단계 --> r,theata ,x ,y 값 출력하기 ----------------------
        # min_deg = theata_rad[min_idx] * 180 / math.pi
        # rospy.loginfo("\nminimum range (r, theata , x , y) = {:.3f} {:.3f} {:.3f} {:.3f}".format(min_range, min_deg , x, y))
        
        #입력된 LIDAR 데이터 중, 차량 정면에 해당하는 부분의 데이터가 일정 거리 이하일 경우, 위험하다는 메세지를 전달
        #확인해야할 내용: 차량 정면에 해당하는 부분이 어디까지 인지를 정해야함 ( 라이다 감지 범위 설정 ( 각도 또는 X,Y기준 ))
        #일정 거리를 몇으로 할지 , 하나만 들어와도 위험하다고 할지 아니면 여러개가 들어와야 위험하다고 할지 
        
        # MIN_ANGLE = -179
        # MAX_ANGLE = -135
        # MIN2_ANGLE = 135
        # MAX_2_ANGLE = 179
        # WARNING_RANGE = 1
        # WARNING_CNT = 10
        
        # theata_deg = []
        # for i in range(len(_data.ranges)):
        #     tmp_theata = _data.angle_min + i * _data.angle_increment
        #     if tmp_theata >= _data.angle_max:
        #         tmp_theata = _data.angle_max
        #     theata_deg.append(tmp_theata*180/math.pi)
        # rospy.loginfo(theata_deg)
        # # rospy.loginfo(len(_data.ranges))
        
        # point_cnt = 0
        # for i, distance in enumerate(_data.ranges):
        #     if MIN_ANGLE <= theata_deg[i] <= MAX_ANGLE or MIN2_ANGLE <= theata_deg[i] <= MAX_2_ANGLE:
        #         if distance < WARNING_RANGE:
        #             point_cnt += 1
                    
        
                    
        # if point_cnt >= WARNING_CNT:
        #     self.warning_pub.publish("Warning")
        #     rospy.loginfo("Warning")
        # else:
        #     self.warning_pub.publish("Safe")
        #     rospy.loginfo("Safe")
        
        
        

def run(): #실제 코드 동작 시 , 실행할 부분
    rospy.init_node("lidar_example") # ros master에 노드 등록하는 함수
    new_class = LidarReceiver() #실제 동작을 담당하는 object
    rospy.spin() # ros node가 종료되지 않고, callback함수를 정상적으로 실행해주는 함수
    

if __name__ == '__main__': # 해당 python코드를 직접 실행할 때만 동작하도록 하는 함수
    run() # 실제 동작하는 코드 
    
    
    

