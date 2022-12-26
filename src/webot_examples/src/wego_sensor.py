#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import numpy as np
from std_msgs.msg import Int32MultiArray
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Image, Imu
from tf.transformations import euler_from_quaternion
from cv_bridge import CvBridge
from ackermann_msgs.msg import AckermannDriveStamped

class WegoSensor():
    
    def __init__(self):
        self.img = None
        self.bridge = CvBridge()
        self.img_sub = rospy.Subscriber("/usb_cam/image_raw",Image, self.camera_callback)
        
        self.imu = None
        self.imu_sub = rospy.Subscriber("imu", Imu, self.imu_callback)
        
        self.lidar = None
        self.lidar_sub = rospy.Subscriber("/scan", LaserScan, self.lidar_callback)
        
    
    def camera_callback(self, _img):
        self.img = self.bridge.imgmsg_to_cv2(_img, "bgr8")
        
    def lidar_callback(self, _data):
        self.angle_min = _data.angle_min
        self.angle_max = _data.angle_max
        self.angle_increment = _data.angle_increment
        self.time_increment = _data.time_increment
        self.scan_time = _data.scan_time
        self.range_min = _data.range_min
        self.range_max = _data.range_max
        self.lidar = _data.ranges
        
    def imu_callback(self, _msg):
        _,_, yaw = euler_from_quaternion((_msg.orientation.x, _msg.orientation.y,_msg.orientation.z,_msg.orientation.w))
        self.yaw = yaw % (2*np.pi)
        
        
        
        