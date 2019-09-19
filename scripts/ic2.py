from smbus import SMBus
import time

temp = "a"
count = 1

time.sleep(1)
addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1

while True:
	temp = raw_input("Press any key to turn LED on/of: ")
	print("Temp = " + temp)
	print(type(0x1))
	if temp == "1":
		bus.write_byte(addr, 0x1) # switch it on
	elif temp == "2":
                bus.write_byte(addr, 0x2) # switch it on
	else:
                bus.write_byte(addr, 0x3) # switch it on

