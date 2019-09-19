#!/usr/bin/env python
# Software License Agreement (BSD License)
#

## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy
from std_msgs.msg import String
import csv

pulley_status = 0
exit_status = 0

dataset = {"12345a": "Apples", "12345b": "Bacon", "12345c": "Chicken", "12345d": "Dates", "abcd1": "Basket1", "abcd2": "Basket2", "abcd3": "Basket3", "abcd4": "Basket4"}

pub = rospy.Publisher('servo_exit', String, queue_size=10)

def print_db():
    with open('SupermarketDB.csv', 'rb') as csvfile:
	db = csv.reader(csvfile, delimiter=' ')
	for row in db:
		print ', '.join(row)

def rfid1(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
    temp_db = []

    with open('SupermarketDB.csv', 'rb') as csvfile:
        db = csv.reader(csvfile, delimiter=' ')
        for row in db:
		temp_db.append(row)
  
    global pulley_status   
 
    if pulley_status == 0:
	pulley_status = 1
	print("User activated!")
	
	if data.data == '24019189112':
		print('First user!')
		temp_db[0][1] = 1
	elif data.data == '32128254112':
                print('Second user!')
		temp_db[1][1] = 1
    	with open('SupermarketDB.csv', 'wb') as csvfile:
		db = csv.writer(csvfile, delimiter=' ')
		for row in temp_db:
			db.writerow(row)	

    else:
	pulley_status = 0
	print("User finished with task")
	
	if data.data == '24019189112':
                print('First user!')
                temp_db[0][1] = 0
        elif data.data == '32128254112':
                print('Second user!')
                temp_db[1][1] = 0
        with open('SupermarketDB.csv', 'wb') as csvfile:
                db = csv.writer(csvfile, delimiter=' ')
                for row in temp_db:
                        db.writerow(row)

    rospy.loginfo("Pulley new status: " + str(pulley_status))
    print_db()	
    rospy.loginfo("\n\n")

def rfid2(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
    temp_db = []

    with open('SupermarketDB.csv', 'rb') as csvfile:
        db = csv.reader(csvfile, delimiter=' ')
        for row in db:
                temp_db.append(row)

    global exit_status

    if exit_status == 0:
        exit_status = 1
        print("Exit activated!")

        if data.data == '24019189112':
                print('First user!')
                temp_db[0][1] = 2
        elif data.data == '32128254112':
                print('Second user!')
                temp_db[1][1] = 2
        with open('SupermarketDB.csv', 'wb') as csvfile:
                db = csv.writer(csvfile, delimiter=' ')
                for row in temp_db:
                        db.writerow(row)

    else:
        exit_status = 0
        print("User finished with task")

        if data.data == '24019189112':
                print('First user!')
                temp_db[0][1] = 0
        elif data.data == '32128254112':
                print('Second user!')
                temp_db[1][1] = 0
        with open('SupermarketDB.csv', 'wb') as csvfile:
                db = csv.writer(csvfile, delimiter=' ')
                for row in temp_db:
                        db.writerow(row)

    rospy.loginfo("New Exit status: " + str(pulley_status))
    print_db()
    rospy.loginfo("\n\n")

def barcode1(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
    temp_db = []

    with open('SupermarketDB.csv', 'rb') as csvfile:
        db = csv.reader(csvfile, delimiter=' ')
        for row in db:
                temp_db.append(row)

    if temp_db[0][1] == '1':
	temp_db[0].append(dataset[data.data])
    elif temp_db[1][1] == '1':
	temp_db[1].append(dataset[data.data])

    elif temp_db[0][1] == '2':
	temp_db[0].remove(dataset[data.data])
	pub.publish('1')
    elif temp_db[1][1] == '2':
        temp_db[1].remove(dataset[data.data])
	pub.publish('2')

    
    with open('SupermarketDB.csv', 'wb') as csvfile:
	db = csv.writer(csvfile, delimiter=' ')
	for row in temp_db:
		db.writerow(row)

    print_db()
    rospy.loginfo("\n\n")

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('entry_node', anonymous=True)

    rospy.Subscriber('rfid_entry', String, rfid1)
    rospy.Subscriber('barcode_entry', String, barcode1)
    rospy.Subscriber('rfid_exit', String, rfid2)
    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()
    while not rospy.is_shutdown():
	pass
	#pub.publish("HI")
	#rospy.sleep(1)

if __name__ == '__main__':
    listener()
