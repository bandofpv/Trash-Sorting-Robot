import serial
import cv2

port = "/dev/ttyACM0"
rate = 9600

s1 = serial.Serial(port,rate)
s1.flushInput()


comp_list=["Flash complete\r\n","Connected to Arduino\r\n"]


while True:
	if s1.inWaiting()>0:
		inputValue = s1.readline()
		print(inputValue.decode())
		if inputValue.decode() in comp_list:
			try:
				n = bytes(input("Set Flash Times:"), 'utf-8')
				s1.write(n)
			except:
				print("Input error, please input a number")
				s1.write(bytes('0', 'utf-8'))
