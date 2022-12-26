#!/usr/bin/env python
#-*- coding: utf-8 -*-

import rospy
from ackermann_msgs.msg import AckermannDriveStamped
from std_msgs.msg import Int32, String, Bool ,Float32
import time
#publisher 1개가 필요
# topic name =  /high_level_ackermann_cmd_mux/input/nav_0 
# topic msg type = ackermann_msgs/AckermannDriveStamped
# steering_angle = 입력 가능한 범위 -0.34 ~ +0.34
# speed = 시뮬레이터 기준 -2.5 ~ +2.5   실차량 기준은 -10 ~ 10 m/s

class Controller():
    def __init__(self):
       self.right_lane_x = 0
       self.ref_rad = 0
       self.ref_right_lane_x = 225 
       self.warning = False
       self.slow_vehicle = False
       self.no_change = False
       self.right_change = False
       self.left_change = False
       self.center = False
       self.drive_pub = rospy.Publisher("high_level/ackermann_cmd_mux/input/nav_0", AckermannDriveStamped, queue_size=1)
       rospy.Subscriber("right_lane_moment_x", Int32, self.lane_callback)
       rospy.Subscriber("Obstacle_mission", String, self.change_callback)
       rospy.Subscriber("Slow_down_mission", Bool, self.slow_callback)
       rospy.Subscriber("corn_mission",Float32,self.corn_callback)
       rospy.Timer(rospy.Duration(1.0/5),self.timer_callback)
       self.rate = rospy.Rate(1.0/5)
       self.get_time = rospy.get_rostime().secs
     #   while not rospy.is_shutdown():
     #       self.publish_data() 
     #       self.rate.sleep()
           
           
    def lane_callback(self,_data):
        self.right_lane_x = _data.data
     
     
    def slow_callback(self, _data):
          if _data.data == False:
               self.slow_vehicle = False
          elif _data.data == True:
               self.slow_vehicle = True
          else:
               rospy.loginfo("Unknown slow state")

    def change_callback(self,_data):
         if _data.data == "right":
              self.right_change = True
              self.left_change = False
              self.no_change = False
              self.center = False
         elif _data.data == "left":
               self.left_change = True
               self.right_change = False
               self.no_change = False
               self.center = False
         elif _data.data == "none":
               self.no_change = True
               self.left_change = False
               self.right_change = False
         elif _data.data == "center":
               self.center = True
               self.no_change = False
               self.left_change = False
               self.right_change = False
               
     
    def corn_callback(self,_data):
          self.ref_rad = _data.data

               
    
    def timer_callback(self,_event):
       if self.slow_vehicle:
              self.slow()
              rospy.loginfo("slow_lane")
              
       elif self.right_change or self.left_change:
            self.corn_lane()
            rospy.loginfo("corn object detected")
     
       elif self.center:
            self.change_lane()
            rospy.loginfo("change objecet detected")
            

       elif self.no_change:
              self.follow_lane()
              rospy.loginfo("follow_lane")
              
       else: 
            self.follow_lane()
            rospy.loginfo("def follow_lane")
     
          
         

    def slow(self):
         self.error_lane = self.ref_right_lane_x - self.right_lane_x  
         #error가 음수 -> 오른쪽 차선이랑 멀다 --> 오른쪽으로 붙어야 한다 --> 바퀴를 오른쪽으로 회전해야 한다 --> steering_angle이 음수 
         #error가 양수 -> 오른쪽 차선이랑 가깝다 --> 오른쪽에서 멀어져야 한다 --> 바퀴를 왼쪽으로 회전해야 한다 --> steering_angle이 양수
         rospy.loginfo("error_lane = {}".format(self.error_lane))
         publishing_data = AckermannDriveStamped()
         publishing_data.header.stamp = rospy.Time.now()
         publishing_data.header.frame_id = "base_link"
         publishing_data.drive.steering_angle = self.error_lane * 0.003
         publishing_data.drive.speed = 0.2
         self.drive_pub.publish(publishing_data)
         rospy.loginfo("slow_lane data")
         
    def right_lane(self):
         publishing_data = AckermannDriveStamped()
         publishing_data.header.stamp = rospy.Time.now()
         publishing_data.header.frame_id = "base_link"
         publishing_data.drive.steering_angle = -0.1
         publishing_data.drive.speed = 0.3
         self.drive_pub.publish(publishing_data)
         rospy.loginfo("right_change")
         
    def change_lane(self):
         
         for i in range(35):
               publishing_data = AckermannDriveStamped()
               publishing_data.header.stamp = rospy.Time.now()
               publishing_data.header.frame_id = "base_link"
               publishing_data.drive.steering_angle = 0.2
               publishing_data.drive.speed = 0.3
               self.drive_pub.publish(publishing_data)
               rospy.loginfo("left_change")
               time.sleep(0.05)

         for h in range(50):
               publishing_data = AckermannDriveStamped()
               publishing_data.header.stamp = rospy.Time.now()
               publishing_data.header.frame_id = "base_link"
               publishing_data.drive.steering_angle = -0.2
               publishing_data.drive.speed = 0.3
               self.drive_pub.publish(publishing_data)
               rospy.loginfo("right_change")
               time.sleep(0.05)
               
         for j in range(10):
               publishing_data = AckermannDriveStamped()
               publishing_data.drive.speed = 0.4
               self.drive_pub.publish(publishing_data)
               rospy.loginfo("go_straight")
               time.sleep(0.05)
               
         for h in range(40):
               publishing_data = AckermannDriveStamped()
               publishing_data.header.stamp = rospy.Time.now()
               publishing_data.header.frame_id = "base_link"
               publishing_data.drive.steering_angle = -0.2
               publishing_data.drive.speed = 0.3
               self.drive_pub.publish(publishing_data)
               rospy.loginfo("right_change")
               time.sleep(0.05)
               
         for i in range(38):
               publishing_data = AckermannDriveStamped()
               publishing_data.header.stamp = rospy.Time.now()
               publishing_data.header.frame_id = "base_link"
               publishing_data.drive.steering_angle = 0.2
               publishing_data.drive.speed = 0.3
               self.drive_pub.publish(publishing_data)
               rospy.loginfo("left_change")
               time.sleep(0.05)
               
         for i in range(35):
               self.error_lane = self.ref_right_lane_x - self.right_lane_x 
               publishing_data = AckermannDriveStamped()
               publishing_data.header.stamp = rospy.Time.now()
               publishing_data.header.frame_id = "base_link"
               publishing_data.drive.steering_angle = 0.0
               publishing_data.drive.speed = 0.4
               self.drive_pub.publish(publishing_data)
               rospy.loginfo("go_straight")
               time.sleep(0.05)
               
         time.sleep(1)
              
               
              
              
         
    def left_lane(self):
        publishing_data = AckermannDriveStamped()
        publishing_data.header.stamp = rospy.Time.now()
        publishing_data.header.frame_id = "base_link"
        publishing_data.drive.steering_angle = 0.1
        publishing_data.drive.speed = 0.3
        self.drive_pub.publish(publishing_data)
        rospy.loginfo("left_change")
         
          
    def stop(self):
         publishing_data = AckermannDriveStamped()
         publishing_data.header.stamp = rospy.Time.now()
         publishing_data.header.frame_id = "base_link"
         publishing_data.drive.steering_angle = 0.0
         publishing_data.drive.speed = 0.0
         self.drive_pub.publish(publishing_data)
         rospy.loginfo("Stop data")
    
    def follow_lane(self):
         self.error_lane = self.ref_right_lane_x - self.right_lane_x  
         #error가 음수 -> 오른쪽 차선이랑 멀다 --> 오른쪽으로 붙어야 한다 --> 바퀴를 오른쪽으로 회전해야 한다 --> steering_angle이 음수 
         #error가 양수 -> 오른쪽 차선이랑 가깝다 --> 오른쪽에서 멀어져야 한다 --> 바퀴를 왼쪽으로 회전해야 한다 --> steering_angle이 양수
         rospy.loginfo("error_lane = {}".format(self.error_lane))
         publishing_data = AckermannDriveStamped()
         publishing_data.header.stamp = rospy.Time.now()
         publishing_data.header.frame_id = "base_link"
         publishing_data.drive.steering_angle = self.error_lane * 0.002
         publishing_data.drive.speed = 0.4
         self.drive_pub.publish(publishing_data)
         self.follow_time = rospy.get_rostime().secs
         rospy.loginfo("Publish data")

    def corn_lane(self):
         self.error_lane = self.ref_rad  
         
         #error가 음수 -> 오른쪽 차선이랑 멀다 --> 오른쪽으로 붙어야 한다 --> 바퀴를 오른쪽으로 회전해야 한다 --> steering_angle이 음수 
         #error가 양수 -> 오른쪽 차선이랑 가깝다 --> 오른쪽에서 멀어져야 한다 --> 바퀴를 왼쪽으로 회전해야 한다 --> steering_angle이 양수
         rospy.loginfo("error_lane = {}".format(self.error_lane))
         publishing_data = AckermannDriveStamped()
         publishing_data.header.stamp = rospy.Time.now()
         publishing_data.header.frame_id = "base_link"
         publishing_data.drive.steering_angle = self.error_lane * 0.4
         publishing_data.drive.speed = 0.3
         self.drive_pub.publish(publishing_data)
     #     self.corn_time = rospy.get_rostime().secs
  
         rospy.loginfo("Publish data")
         
         
def run():
    rospy.init_node("control_example")
    Controller()
    rospy.spin()

if __name__ == '__main__':
    run()

