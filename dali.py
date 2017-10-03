import RPi.GPIO as GPIO
import time

BIT_DELAY=0.00034

def send_start(gpio_tx_line):
    global BIT_DELAY
    GPIO.output(GPIO_TX_LINE,GPIO.LOW)
    time.sleep(BIT_DELAY)
    GPIO.output(GPIO_TX_LINE,GPIO.HIGH)
    time.sleep(BIT_DELAY)

def send_1(gpio_tx_line):
    global BIT_DELAY
    GPIO.output(GPIO_TX_LINE,GPIO.LOW)
    time.sleep(BIT_DELAY)
    GPIO.output(GPIO_TX_LINE,GPIO.HIGH)
    time.sleep(BIT_DELAY)

def send_0(gpio_tx_line):
    global BIT_DELAY
    GPIO.output(GPIO_TX_LINE,GPIO.HIGH)
    time.sleep(BIT_DELAY)
    GPIO.output(GPIO_TX_LINE,GPIO.LOW)
    time.sleep(BIT_DELAY)

def send_stop(gpio_tx_line):
    global BIT_DELAY
    GPIO.output(GPIO_TX_LINE,GPIO.HIGH)
    time.sleep(BIT_DELAY)
    GPIO.output(GPIO_TX_LINE,GPIO.HIGH)
    time.sleep(BIT_DELAY)

#GPIO used
GPIO_RX_LINE=30
GPIO_TX_LINE=31

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(GPIO_TX_LINE,GPIO.OUT)

# Initial state
GPIO.output(GPIO_TX_LINE,GPIO.LOW)

#Start bit 
send_start(GPIO_TX_LINE)

#Address bit 0x02
send_0(GPIO_TX_LINE)
send_0(GPIO_TX_LINE)
send_0(GPIO_TX_LINE)
send_0(GPIO_TX_LINE)
send_0(GPIO_TX_LINE)
send_0(GPIO_TX_LINE)
send_1(GPIO_TX_LINE)
send_0(GPIO_TX_LINE)

#Data bit 0x00
send_0(GPIO_TX_LINE)
send_0(GPIO_TX_LINE)
send_0(GPIO_TX_LINE)
send_0(GPIO_TX_LINE)
send_0(GPIO_TX_LINE)
send_0(GPIO_TX_LINE)
send_0(GPIO_TX_LINE)
send_1(GPIO_TX_LINE)

#2 stop bits
send_stop(GPIO_TX_LINE)
send_stop(GPIO_TX_LINE)

#Final state
GPIO.output(GPIO_TX_LINE,GPIO.LOW)
