#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import RPi.GPIO as GPIO
import signal
import time
import serial 

continue_reading = True

ser = serial.Serial('/dev/ttyACM0', 9600)

# Welcome message
print "Welcome to RFID1 System..."
print "Awaiting RFID on Arduino to be scanned...\n\n"

def talker():
    pub = rospy.Publisher('rfid_entry', String, queue_size=10)
    rospy.init_node('rfid_1', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        if (ser.in_waiting > 0):
		full_uid = ser.readline()
		full_uid = full_uid.rstrip()
    		#hello_str = "hello world %s" % rospy.get_time()
        	#rospy.loginfo(hello_str)
		rospy.loginfo(full_uid)
        	pub.publish(full_uid)
		time.sleep(1)
        	rate.sleep()




        #hello_str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(hello_str)
        #pub.publish(hello_str)
        #rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
