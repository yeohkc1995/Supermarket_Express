import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600)

while True:
	ser.write('1')
	print("Data sent HI!")
	time.sleep(3)
	ser.write('2')
        print("Data sent LO!")
        time.sleep(3)


