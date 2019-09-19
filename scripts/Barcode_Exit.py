#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.

import rospy
from std_msgs.msg import String
import sys
import requests
import json
from Tkinter import *
import csv

class Application(Frame):

    #index 1 -> apples, 2 -> bacon, 3 -> chicken, 4 -> dates
    current_list = [0, 0, 0, 0]
    items_str = ""

    def clear_text(self, *args):
        print(self.barcode_input.get())
        self.barcode_input.delete(0, 'end')

    def change_page_1(self):
        self.bg.lift()

    def change_page_2(self):
        self.bg_2.lift()
        self.barcode_input.lift()
        self.enter_button.lift()
	self.text.lift()
	self.text_total.lift()
	self.pay_button.lift()
	self.modify_button.lift()

    def createWidgets(self):

        """
        ---------------- Page 1 -----------------
        """
        self.bg_image = PhotoImage(file='exit_p1_resized.png')
        self.bg = Label(self, image = self.bg_image)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg.pack()


        """
        ---------------- Page 2 -----------------
        """

        self.bg_image_2 = PhotoImage(file='exit_p2_resized.png')
        self.bg_2 = Label(self, image=self.bg_image_2)
        self.bg_2.place(x=0, y=0, relwidth=1, relheight=1)

        self.barcode_input = Entry(self, bg="grey")
        self.barcode_input.place(x = 550, y = 350, height = 30, width = 120)
        self.barcode_input.bind('<Return>', self.talker)
        self.barcode_input.focus()

        self.search_image = PhotoImage(file='search_resized.png')
        self.enter_image = PhotoImage(file='search_resized.png')
        self.enter_button = Button(self, image=self.search_image)
        self.enter_button.place(x=670, y=350, height=30, width=30)

        self.pay_button = Button(self, bg="green", text="Proceed to payment!", font="Ariel")
        self.pay_button.place(x=520, y=240, height=100, width=200)

	self.modify_button = Button(self, bg="yellow", text="Modify purchase")
	self.modify_button.place(x=80, y=320, height=30, width=140)	

        self.text = Label(self, font = ("Courier", 10), bg = "white", anchor = 'w', justify = "left", fg = "blue")
        self.text.place(x = 110, y = 170)

        self.text_total = Label(self, font = ("Courier", 20), bg = "white", anchor = 'w', justify = "left", text = "$0.00", fg = "red")
        self.text_total.place(x = 350, y = 320)
	
	"""
	--------------- Clock Function to check CSV for page refresh -------------
	"""
    def update_clock(self):
        #print("hihihi")
	#self.talker("KCCCCCC")

	temp_db = []

	with open('SupermarketDB.csv', 'rb') as csvfile:
        	db = csv.reader(csvfile, delimiter=' ')
        	for row in db:
                	temp_db.append(row)

    	if ( (temp_db[0][1] == '2') or (temp_db[1][1] == '2') ):
		self.change_page_2()
		self.update_text()
	else:
		self.change_page_1()

	self.after(1000, self.update_clock)

    def update_text(self):

	self.items_str = ""
        temp_db = []
	temp_db_2 = []
        self.current_list = [0,0,0,0]

        with open('SupermarketDB.csv', 'rb') as csvfile:
            db = csv.reader(csvfile, delimiter=' ')
            for row in db:
                temp_db.append(row)

        if (temp_db)[0][1] == '2':
            temp_db_2 = temp_db[0]
        elif (temp_db[1][1]) == '2':
            temp_db_2 = temp_db[1]

        del temp_db_2[0:2]

        while len(temp_db_2) > 0:
            temp_item = temp_db_2.pop()

            if temp_item == "Apples":
                self.current_list[0] += 1
            elif temp_item == "Bacon":
                self.current_list[1] += 1
            elif temp_item == "Chicken":
                self.current_list[2] += 1
            elif temp_item == "Dates":
                self.current_list[3] += 1
	    else:
		pass
        for counter,value in enumerate(self.current_list):
            if value > 0:
                if counter == 0:
                    self.items_str += "Apples \t  $1.50        " + str(value) + "\t" + "$" + str(value *1.5) + "0" + "\n\n"
                elif counter == 1:
                    self.items_str += "Bacon \t  $2.50        " + str(value) + "\t" + "$" + str(value *2.5) + "0" + "\n\n"
                elif counter == 2:
                    self.items_str += "Chicken   $3.00        " + str(value) + "\t" + "$" + str(value *3.0) + "0" + "\n\n"
                elif counter == 3:
                    self.items_str += "Dates \t  $1.00        " + str(value) + "\t" + "$" + str(value *1.0) + "0" + "\n\n"
	
	self.text['text'] = self.items_str

	total_cost = self.current_list[0] * 1.5 + self.current_list[1] * 2.5 + self.current_list[2] * 3 + self.current_list[3] * 1
	total_cost = "$" + str(total_cost) + "0"
	self.text_total['text'] = str(total_cost)
	"""
	--------------- ROS Publish Function ----------------
	"""
    def talker(self, *args):
    	pub = rospy.Publisher('barcode_entry', String, queue_size=10)
    	rospy.init_node('talker', anonymous=True)
    	rate = rospy.Rate(10) # 10hz
        hello_str = self.barcode_input.get()
        rospy.loginfo("Sending info...")
        pub.publish(hello_str)
	self.barcode_input.delete(0, 'end')


	"""
	-------------- Initialization of App -----------------
	"""
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.change_page_1()
        self.update_clock()

root = Tk()


app = Application(master=root)

app.mainloop()
print("Testtest")
root.destroy()

