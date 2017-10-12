#!/usr/bin/python
#http://info.kmtronic.com/kmtronic-rs485-relays-commands.html

import serial
import time

ser = serial.Serial(
		port='/dev/ttyUSB2', 
		baudrate=9600, 
		timeout=1,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS
)
ser.flushOutput()
ser.flushInput()

while True:
	for i in range(9):
		print "ON"
		sample = "%c%c%c\r" % (0xFF,i,0x01);
		ser.write(sample)
		time.sleep(0.1)
	
		print "OFF"
		sample = "%c%c%c\r" % (0xFF,i,0x00);
		ser.write(sample)
		time.sleep(0.1)
