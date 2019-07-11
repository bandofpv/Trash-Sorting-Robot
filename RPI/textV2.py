#!/usr/bin/env python
import serial

port = "/dev/ttyACM0"
rate = 9600

s1 = serial.Serial(port,rate)
s1.flushInput()


comp_list=["Done turning arm\r\n","Connected to Arduino\r\n"]

while True:
    if s1.inWaiting()>0:
	inputValue = s1.readline()
	print(inputValue)
	if inputValue in comp_list:
	    try:
	        n = input("Set Servo Angle:")
	        s1.write('%d'%n)
	    except:
		print("ERROR: enter a number from 1 - 180")
		s1.write('0')
