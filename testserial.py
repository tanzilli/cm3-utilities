#!/usr/bin/python
import serial
import time

ser=[0,0,0,0]

for i in range(4):
        print i
        ser[i] = serial.Serial(
                port='/dev/ttyUSB%d' % i, 
                baudrate=9600, 
                timeout=1,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
        )
        ser[i].flushOutput()
        ser[i].flushInput()

while True:
        for i in range(4):
                sample = "%d%d%d%d%d%d%d%d%d%d\r" % (i,i,i,i,i,i,i,i,i,i);
                ser[i].write(sample)
                print sample