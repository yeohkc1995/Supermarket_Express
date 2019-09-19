#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import csv


continue_reading = True
user_status = 0

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

def talker():
    global user_status
    pub = rospy.Publisher('rfid_exit', String, queue_size=10)
    rospy.init_node('rfid_2', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        
        # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    	# If a card is found
        if status == MIFAREReader.MI_OK:
        	print "Card detected"
    
    	# Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

    	# If we have the UID, continue
        if status == MIFAREReader.MI_OK:

        	# Print UID

		full_uid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
    
        	# This is the default key for authentication
        	key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        	# Select the scanned tag
        	MIFAREReader.MFRC522_SelectTag(uid)

        	# Authenticate
        	status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
		#hello_str = "hello world %s" % rospy.get_time()
        	#rospy.loginfo(hello_str)
		rospy.loginfo("UID:")
		rospy.loginfo(full_uid)
		rospy.loginfo("\n\n")
        	pub.publish(full_uid)
		time.sleep(1)
        	rate.sleep()

        	# Check if authenticated
        	if status == MIFAREReader.MI_OK:
            		MIFAREReader.MFRC522_Read(8)
            		MIFAREReader.MFRC522_StopCrypto1()
        	else:
            		print "Authentication error" 



        #hello_str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(hello_str)
        #pub.publish(hello_str)
        #rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
