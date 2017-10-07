import os.path
import smbus
import time

## Display 16x2 Winstar

class lcd():

	lcd_address = 0x3E

	def __init__(self,i2c_bus_id):
		self.i2c_bus = smbus.SMBus(i2c_bus_id)
		self.sendcommand(0x38)
		self.sendcommand(0x39)
		self.sendcommand(0x14) #Internal OSC freq
		self.sendcommand(0x72) #Set contrast 
		self.sendcommand(0x54) #Power/ICON control/Contrast set
		self.sendcommand(0x6F) #Follower control
		self.sendcommand(0x0C) #Display ON
		self.clear()
		return

	def sendcommand(self,value):
		self.i2c_bus.write_byte_data(self.lcd_address,0x00,value)
		return

	def senddata(self,value):
		self.i2c_bus.write_byte_data(self.lcd_address,0x40,value)
		return

	def clear(self):
		self.sendcommand(0x01)
		time.sleep(0.001)
		return

	def home(self):
		self.sendcommand(0x03)
		time.sleep(0.001)
		return

	def setcontrast(self,value):
		self.sendcommand(0x70 + value)
		return

	def setdoublefont(self):
		self.sendcommand(0x30 + 0x0C + 0x01)
		return

	def setsinglefont(self):
		self.sendcommand(0x30 + 0x08 + 0x01)
		return

	def setcurpos(self,x,y):
		if y<0 or y>1:
			return
		if x<0 or x>15:
			return

		if y==0:
			self.sendcommand(0x80+0x00+x)
		else:
			self.sendcommand(0x80+0x40+x)
		return

	def putchar(self,value):
		self.senddata(value)
		return

	def putstring(self,string):
		if len(string)==0:
			return
		if len(string)>16:
			string=string[0:16]

		for char in string:
			self.putchar(ord(char))
		return

