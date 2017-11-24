#!/usr/bin/python
# Documentazione comandi DALI
# http://www.tanzolab.it/www/CM3-HOME_test/dali_commands.pdf

import RPi.GPIO as GPIO
import time
import sys

BIT_DELAY=0.00034

#GPIO line used
GPIO_TX_LINE=31

def send_start():
    global BIT_DELAY
    global GPIO_TX_LINE
    
    GPIO.output(GPIO_TX_LINE,GPIO.LOW)
    time.sleep(BIT_DELAY)
    GPIO.output(GPIO_TX_LINE,GPIO.HIGH)
    time.sleep(BIT_DELAY)

def send_1():
    global BIT_DELAY
    global GPIO_TX_LINE

    GPIO.output(GPIO_TX_LINE,GPIO.LOW)
    time.sleep(BIT_DELAY)
    GPIO.output(GPIO_TX_LINE,GPIO.HIGH)
    time.sleep(BIT_DELAY)

def send_0():
    global BIT_DELAY
    global GPIO_TX_LINE

    GPIO.output(GPIO_TX_LINE,GPIO.HIGH)
    time.sleep(BIT_DELAY)
    GPIO.output(GPIO_TX_LINE,GPIO.LOW)
    time.sleep(BIT_DELAY)

def send_stop():
    global BIT_DELAY
    global GPIO_TX_LINE

    GPIO.output(GPIO_TX_LINE,GPIO.HIGH)
    time.sleep(BIT_DELAY)
    GPIO.output(GPIO_TX_LINE,GPIO.HIGH)
    time.sleep(BIT_DELAY)

def send_value(value):
	global BIT_DELAY
	global GPIO_TX_LINE

	for i in range(8):
		value=value&0xFF
		#print "%02x" % value 
		if (value & 0x80) == 0:
			send_0()
			#print "send 0"
		else:		
			send_1()
			#print "send 1"
		value=value<<1

def send_short_address(addr):
	global BIT_DELAY
	global GPIO_TX_LINE

	# Send first byte
	send_0() # Y=0 Short Address
	
	# Send 6 bit address. Most first
	if addr & 0x20:
		send_1()
	else:
		send_0()

	if addr & 0x10:
		send_1()
	else:
		send_0()

	if addr & 0x8:
		send_1()
	else:
		send_0()

	if addr & 0x4:
		send_1()
	else:
		send_0()
		
	if addr & 0x2:
		send_1()
	else:
		send_0()
	
	if addr & 0x1:
		send_1()
	else:
		send_0()
	
	send_0() # A=0 Direct arc power level


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(GPIO_TX_LINE,GPIO.OUT)

# Initial state
GPIO.output(GPIO_TX_LINE,GPIO.HIGH)


send_start()
send_short_address(22)
send_value(0)
send_stop()
send_stop()
time.sleep(0.001)

send_start()
send_short_address(23)
send_value(0)
send_stop()
send_stop()
time.sleep(0.001)

send_start()
send_short_address(24)
send_value(0)
send_stop()
send_stop()
time.sleep(0.001)

send_start()
send_short_address(25)
send_value(0)
send_stop()
send_stop()

time.sleep(0.001)

LED_GREEN=22
LED_RED=23
LED_BLUE=24

#Demo mode
if len(sys.argv)==1:
	print "Demo mode"
	print "Add --help for the command syntax"
	
	for i in range(1):
		for i in range(0,255,1):
			send_start()
			send_short_address(LED_RED)
			send_value(i)
			send_stop()
			send_stop()
			time.sleep(0.001)
			
		for i in range(255,-1,-1):
			send_start()
			send_short_address(LED_RED)
			send_value(i)
			send_stop()
			send_stop()
			time.sleep(0.001)

		for i in range(0,255,1):
			send_start()
			send_short_address(LED_GREEN)
			send_value(i)
			send_stop()
			send_stop()
			time.sleep(0.001)

		for i in range(255,-1,-1):
			send_start()
			send_short_address(LED_GREEN)
			send_value(i)
			send_stop()
			send_stop()
			time.sleep(0.001)

		for i in range(0,255,1):
			send_start()
			send_short_address(LED_BLUE)
			send_value(i)
			send_stop()
			send_stop()
			time.sleep(0.001)

		for i in range(255,-1,-1):
			send_start()
			send_short_address(LED_BLUE)
			send_value(i)
			send_stop()
			send_stop()
			time.sleep(0.001)

			#Final state 
			GPIO.output(GPIO_TX_LINE,GPIO.HIGH)

if len(sys.argv)==2 and sys.argv[1]:
	print "daly.py -r=(0-255) -g=(0-255) -b=(0-255)"

if len(sys.argv)==4:
	print sys.argv[1]
	print sys.argv[2]
	print sys.argv[3]

#Final state 
GPIO.output(GPIO_TX_LINE,GPIO.HIGH)
