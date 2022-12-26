#!/usr/bin/env python 
#-*- coding: utf-8 -*- 

import rospy
from sensor_msgs.msg import CompressedImage,CameraInfo 
from vision_msgs.msg import Detection2DArray
from std_msgs.msg import Int32, Float32, Bool

class SlowReciver():
    df = Bool()

    def __init__(self):
        rospy.loginfo("aruco object is detected")
        rospy.Subscriber("fiducial_transforms", Detection2DArray , self.slow_callback)
        self.slow_pub = rospy.Publisher("Slow_down_mission", Bool)
        self.aruco_detcet = False
        self.get_time = rospy.get_rostime().secs
        

    def slow_callback(self,_data):
        
        if len(_data.detections) == 0:
            self.aruco_detect = False
            rospy.loginfo("aruco_example not detected")
            # rospy.loginfo("id = {}".format(_data.detections[0].results[0].id))
        else:
            self.get_time = rospy.get_rostime().secs
            if _data.detections[0].results[0].id ==3:
                if _data.detections[0].results[0].pose.pose.position.z < 0.8:
                    self.aruco_detect = True
                    rospy.loginfo("aruco_example is detected")
                    # rospy.loginfo("id = {}".format(_data.detections[0].results[0].id))


        self.time()
                    

# else 부분 
# 검출된 detection id 가 3번인 마크가 존재하는지 확인 
# 존재한다면 z값 
# 1. True 값이 마지막으로 저장된 시간 / 현재 시간 비교해서 True를 지속하도록
# 2. 동작부분에 시간을 늘리거나 
    
        
    def time(self):
        if rospy.get_rostime().secs - self.get_time < 30:
            self.aruco_detect = True
        
        self.slow_pub.publish(self.aruco_detect)
    
    
def run():
    rospy.init_node("slow_down_mission_detector") 
    new_class = SlowReciver()
    rospy.spin() 
    
if __name__ == '__main__': 
    run() 