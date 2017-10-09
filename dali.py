import RPi.GPIO as GPIO
import time

BIT_DELAY=0.00034

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

#GPIO used
GPIO_TX_LINE=31

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(GPIO_TX_LINE,GPIO.OUT)

# Initial state
GPIO.output(GPIO_TX_LINE,GPIO.HIGH)

for i in range(255):
	print i
	
	#Start bit 
	send_start()

	#Send first byte
	send_0() # Y=0 Short Address
	send_0() # Address 2
	send_0()
	send_0()
	send_0()
	send_1() 
	send_0()
	send_0() # A=0 Direct arc power level

	#Data bit
	send_value(i)

	#2 stop bits
	send_stop()
	send_stop()
	
	time.sleep(0.001)

for i in range(255,-1,-1):
	print i
	
	#Start bit 
	send_start()

	#Send first byte
	send_0() # Y=0 Short Address
	send_0() # Address 2
	send_0()
	send_0()
	send_0()
	send_1() 
	send_0()
	send_0() # A=0 Direct arc power level

	#Data bit
	send_value(i)

	#2 stop bits
	send_stop()
	send_stop()
	
	time.sleep(0.001)


#Final state
GPIO.output(GPIO_TX_LINE,GPIO.HIGH)
