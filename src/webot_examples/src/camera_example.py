#!/usr/bin/env python 
#-*- coding: utf-8 -*- 

import rospy # Ros에서 python을 활용할 수 있도록 한 부분 
#sensor_msgs/CompressedImage 타입의 /image_jpeg/compressed 토픽을 받는 코드 작성
from sensor_msgs.msg import CompressedImage , Image# sensor_msgs/Compressed 타입을 사용하기 위해 추가한 부분 
import math 
from std_msgs.msg import Int32
from cv_bridge import CvBridge
import cv2
import numpy as np 

class CameraReciver():
    def __init__(self):
        rospy.loginfo("Camera Receiver Object is Created")
        rospy.Subscriber("/usb_cam/image_rect_color", Image, self.camera_callback)
        self.initialized = False
        self.bridge = CvBridge()
        
        
    def camera_callback(self, _data):
        if self.initialized == False:
            cv2.namedWindow("Simulator_Image", cv2.WINDOW_NORMAL)
            cv2.createTrackbar("low_H", "Simulator_Image", 0 , 255, nothing)
            cv2.createTrackbar("low_S", "Simulator_Image", 0 , 255, nothing)
            cv2.createTrackbar("low_V", "Simulator_Image", 155 , 255, nothing)
            cv2.createTrackbar("high_H", "Simulator_Image", 255 , 255, nothing)
            cv2.createTrackbar("high_S", "Simulator_Image", 255, 255, nothing)
            cv2.createTrackbar("high_V", "Simulator_Image", 255 , 255, nothing)
            self.initialized = True
        # rospy.loginfo(len(_data.data))
        cv_image = self.bridge.compressed_imgmsg_to_cv2(_data)
        # rospy.loginfo(cv_image.shape)
        
        # crop_image = cv_image.copy()[242:480, : , :]
        # cv2.imshow("crop_image", crop_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        crop_image = cv_image.copy()[300:480, 320:640, :]
        
        low_H = cv2.getTrackbarPos("low_H" , "Simulator_Image")
        low_S = cv2.getTrackbarPos("low_S" , "Simulator_Image")
        low_V = cv2.getTrackbarPos("low_V" , "Simulator_Image")
        high_H = cv2.getTrackbarPos("high_H" , "Simulator_Image")
        high_S = cv2.getTrackbarPos("high_S" , "Simulator_Image")
        high_V= cv2.getTrackbarPos("high_V" , "Simulator_Image")

        lower_lane = np.array([low_H,low_S,low_V])
        upper_lane = np.array([high_H,high_S,high_V])
        
        lane_image =  cv2.inRange(crop_image, lower_lane, upper_lane)
        
        
        M = cv2.moments(lane_image)
        if M['m00'] != 0:
            self.x = int(M['m10']/M['m00'])
            self.y = int(M['m01']/M['m00'])
        else:
            self.x = 0
            self.y = 0
        
        rospy.loginfo("x,y = {}, {}".format(self.x,self.y))
        
        cv2.circle(crop_image, (self.x,self.y), 5, (0,255,0), -1)
        
        cv2.imshow("result_image", crop_image)
        cv2.imshow("Simulator_image",cv_image)
        cv2.imshow("Lane Image", lane_image)
        
        channel_1, channel_2, channel_3 = cv2.split(cv_image)
        cv2.imshow("Simulator_Image, 1" , channel_1)
        cv2.imshow("Simulator_Image, 2" , channel_2)
        cv2.imshow("Simulator_Image, 3" , channel_3)
        
        cv2.waitKey(1)
        
def nothing():
    pass


def run(): #실제 코드 동작 시 , 실행할 부분
    rospy.init_node("camera_example") # ros master에 노드 등록하는 함수
    new_class = CameraReciver() #실제 동작을 담당하는 object
    rospy.spin() # ros node가 종료되지 않고, callback함수를 정상적으로 실행해주는 함수
    

if __name__ == '__main__': # 해당 python코드를 직접 실행할 때만 동작하도록 하는 함수
    run() # 실제 동작하는 코드 
    