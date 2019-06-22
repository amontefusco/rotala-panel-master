#!/usr/bin/python

import sys
# don't let .pyc to going around
sys.dont_write_bytecode = True

import tornado.ioloop
import tornado.web
import tornado.websocket
import time
import threading
import json
import smbus
from Stepper import stepper
from subprocess import call
import traceback

import tornado.options
tornado.options.parse_command_line()


import RPi.GPIO as GPIO # https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
GPIO.setmode(GPIO.BCM)
GPIO.setup(34, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
homePin = GPIO.input(34)
GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
probePin = GPIO.input(31)


ws=None
t_exit=False

I2C_ADDRESS = 0x36

bus = smbus.SMBus(1)

#------stepper variables--------*
#[stepPin, directionPin, enablePin]
runHeight = stepper([25, 26, 29])
runFence = stepper([27, 28, 30])


Height_Actual = 0.0		# Height Display Value
Height_Target = 0.0

Fence_Actual = 0.0		# Fence Display Value
Fence_Target = 0.0

# Position variables
FenceHomePos = 0.0			# Sensor Position for Fence Homing
FenceMaxLimit = 400.0		# Maximum Fence Travel (mechanical limited)
HeightHomePos = 0.0			# Sensor Position for Height Homing ( completely retracted)
HeightMaxLimit = 100.0		# Maximum Fence Travel (mechanical limited)

# Homing Variables
HomeSearchSpeed = 300		# Velocity for initially finding the homing switch
HomeLachingSpeed = 20		# Velocity for latching phase 
HomeLachBackoff = 10		# Distance (mm) to back off switch during latch and for clears
HomeZeroBackoff = 12		# Distance (mm) to back off switch before setting machine coordinate system zero
HomeIgnoreLimits = False	# Set true when Homing
FenceHomeDir = "left"		# Fence Direction when Homing
HeightHomeDir =	"right"		# Height Direction when Homing

# Zero Variables
HeightZero = 0.0
FenceZero = 0.0
TouchPlateDim = 20				# Touch Plate dimension
FenceOffsetRadius = 6			# Set the offset for the touch probe equal to diameter/2 + touch plate dimension
AbsoluteCoordinates = True		# Absolute coordinate system (aka machine coordinate system)
RelativeCoordinates = False		# Set relative mode (Offsets from Absolute Coordinates)
probeDistance = 60				# Preset Max distance when moving for Auto Zero



def MoveFence(ABS):
	print "Thread MoveFence ABS %d" % ABS
	data = {"target": "Center", "value" : "images/RunningToAbs.jpg"}
	data = json.dumps(data)
	ws.write_message(data)
	if ABS > 0:
		runFence.step(ABS*200, "left"); #steps, dir, speed, stayOn
		runFence.cleanGPIO
	else:
		runFence.step(ABS*200, "right"); #steps, dir, speed, stayOn
		runFence.cleanGPIO
	data = {"target": "Center", "value" : "images/RunToAbs.jpg"}
	data = json.dumps(data)
	ws.write_message(data)
	
def MoveFenceRel(ABS):
	data = {"target": "Center3", "value" : "images/MovingRel.jpg"}
	data = json.dumps(data)
	ws.write_message(data)
	if ABS > 0:
		runFence.step(ABS*200, "left"); #steps, dir, speed, stayOn
		runFence.cleanGPIO
	else:
		runFence.step(ABS*200, "right"); #steps, dir, speed, stayOn
		runFence.cleanGPIO
	data = {"target": "Center3", "value" : "images/MoveRel.jpg"}
	data = json.dumps(data)
	ws.write_message(data)


def MoveHeight(ABS):
	data = {"target": "Center2", "value" : "images/RunningToAbs.jpg"}
	data = json.dumps(data)
	ws.write_message(data)
	if ABS > 0:
		runHeight.step(ABS*200, "left"); #steps, dir, speed, stayOn
		runHeight.cleanGPIO
	else:
		runHeight.step(ABS*200, "right"); #steps, dir, speed, stayOn
		runHeight.cleanGPIO
	data = {"target": "Center2", "value" : "images/RunToAbs.jpg"}
	data = json.dumps(data)
	ws.write_message(data)



def fenceFineHoming():
	print('Fence Fine Homing Started')
	GPIO.add_event_detect(34, GPIO.RISING)

	while True:
		runFence.step(1, "left"); #steps, dir, speed, stayOn	
		if GPIO.event_detected(34):
			GPIO.remove_event_detect(34)
			runFence.step(10, "right")
			break
	runFence.cleanGPIO
	data = {"target": "fence_homing", "value" : "images/FenceHomeG.jpg"}
	data = json.dumps(data)
	ws.write_message(data)
	print('Fence Fine Homed')


def fenceHoming():
	global FenceHomePos
	global Fence_Actual
	data = {"target": "fence_homing", "value" : "images/FenceNoHome.jpg"}
	data = json.dumps(data)
	ws.write_message(data)
	print('Fence Homing Started')
	GPIO.add_event_detect(34, GPIO.RISING)
#	try:
	while True:
		runFence.step(100, "left"); #steps, dir, speed, stayOn
		if GPIO.event_detected(34):
			GPIO.remove_event_detect(34)
			time.sleep(0.5)
			runFence.step(150, "right")
			time.sleep(0.5)
			runFence.cleanGPIO
			fenceFineHoming()
			break
#		except KeyboardInterrupt:
			# here you put any code you want to run before the program
			# exits when you press CTRL+C
#			print "Aborted"
#		except:
			# this catches ALL other exceptions including errors.
			# You won't get any error messages for debugging
			# so only use it once your code is working
#			print "Other error or exception occurred!"
#		finally:
#	runFence.cleanGPIO
	print('Fence Homed')
	FenceHomePos = 0.0
	Fence_Actual = 0.1


def heightFineHoming():
	print('Height Fine Homing Started')
	GPIO.add_event_detect(34, GPIO.RISING)
	while True:
		runHeight.step(1, "left"); #steps, dir, speed, stayOn
		if GPIO.event_detected(34):
			GPIO.remove_event_detect(34)
			runHeight.step(10, "right")
			break
	runHeight.cleanGPIO
	data = {"target": "height_homing", "value" : "images/HeightHomeG.jpg"}
	data = json.dumps(data)
	ws.write_message(data)
	print('Height Fine Homed')


def heightHoming():
	global HeightHomePos
	global Height_Actual
	data = {"target": "height_homing", "value" : "images/HeightNoHome.jpg"}
	data = json.dumps(data)
	ws.write_message(data)
	print('Height Homing Started')
	GPIO.add_event_detect(34, GPIO.RISING)
#	try:
	while True:
		runHeight.step(100, "left"); #steps, dir, speed, stayOn	
		if GPIO.event_detected(34):
			GPIO.remove_event_detect(34)
			time.sleep(0.5)
			runHeight.step(150, "right")
			time.sleep(0.5)
			runHeight.cleanGPIO
			heightFineHoming()
			break
#		except KeyboardInterrupt:
			# here you put any code you want to run before the program   
			# exits when you press CTRL+C  
#			print "Aborted"
#		except:
			# this catches ALL other exceptions including errors.  
			# You won't get any error messages for debugging  
			# so only use it once your code is working  
#			print "Other error or exception occurred!"
#		finally:
	print('Height Homed')
	Height_Actual = 0.1
	HeightHomePos = 10
	
	
	
def zeroFence():
	global FenceZero
	global Fence_Actual
	global TouchPlateDim
	global FenceOffsetRadius
	print('Height Zero Started')
	data = {"target": "fence_probe", "value" : "images/ProbeRunning.jpg"}
	data = json.dumps(data)
	ws.write_message(data)
	GPIO.add_event_detect(31, GPIO.RISING)
#	try:
	while True:
		runFence.step(1, "left"); #steps, dir, speed, stayOn
		time.sleep(0.5)
		if GPIO.event_detected(31):
			GPIO.remove_event_detect(31)
#			runFence.step(probeDistance, "right"); #steps, dir, speed, stayOn
#			time.sleep(0.5)
			runFence.cleanGPIO
#			FenceFineZero()
			break	
	print('Fence Zeroed')
	Fence_Actual = TouchPlateDim + FenceOffsetRadius
	FenceZero = 0.0
	data = {"target": "fence_probe", "value" : "images/FenceProbe.jpg"}
	data = json.dumps(data)
	ws.write_message(data)	

def zeroHeight():
	global HeightZero
	global Height_Actual
	data = {"target": "height_probe", "value" : "images/ProbeRunning.jpg"}
	data = json.dumps(data)
	ws.write_message(data)
	print('Height Zero Started')
	GPIO.add_event_detect(31, GPIO.RISING)
#	try:
	while True:
		runHeight.step(1, "left"); #steps, dir, speed, stayOn	
		if GPIO.event_detected(31):
			GPIO.remove_event_detect(31)
#			runHeight.step(probeDistance, "right"); #steps, dir, speed, stayOn
#			time.sleep(0.5)
			runHeight.cleanGPIO
#			heightFineZero()
			break
#		except KeyboardInterrupt:
			# here you put any code you want to run before the program   
			# exits when you press CTRL+C  
#			print "Aborted"
#		except:
			# this catches ALL other exceptions including errors.  
			# You won't get any error messages for debugging  
			# so only use it once your code is working  
#			print "Other error or exception occurred!"
#		finally:
	print('Height Zeroed')
	Height_Actual = 0.1
	HeightZero = 0.0
	data = {"target": "height_probe", "value" : "images/HeightProbe.jpg"}
	data = json.dumps(data)
	ws.write_message(data)	
	

	
def counter():
#	global i
	global Height_Actual
	global Height_Target
	global Fence_Actual
	global Fence_Target

# i, z, r, valori di inizializazione dei display (solo test)
#	z=90  # Height Display
	r=45  # Angle Display (used only for test purpose)

	while True:

# comunicazione I2C con sensore angolare
		#amsb = bus.read_byte_data(I2C_ADDRESS, 0x0e)
		#alsb = bus.read_byte_data(I2C_ADDRESS, 0x0f)

		#value = amsb*256 + alsb
		#angolo =  value*(360.0/4096)

		#print "%04X %d %0.2f %0.1f     \r" % (value,value,(value*(360.0/4096)),angolo/8 ),
		#sys.stdout.flush()

		#time.sleep(0.01) # Time in seconds.

		if t_exit==True:
			print "Bye"
			break
# 	incrementa i valori dei display, utilizzato solo per testare i display. Da rimuovere quando in esecuzione codice reale
		#i = i + 0.1
		#if z > 0.01:
		#	z -= 0.1
		#r=angolo/8  # divide 360 angle to display 45 deg commentato quando manca il sensore
		time.sleep(0.1)



# comunica i valori dei display al pannello.
		if ws<>None:
			data = {"target": "display1", "value" : Fence_Actual}
			data = json.dumps(data)
			ws.write_message(data)

			data = {"target": "display2", "value" : Height_Actual}
			data = json.dumps(data)
			ws.write_message(data)

			data = {"target": "display3", "value" : r}
			data = json.dumps(data)
			ws.write_message(data)

			data = {"target": "display4", "value" : Fence_Actual}
			data = json.dumps(data)
			ws.write_message(data)

			data = {"target": "display5", "value" : Height_Actual}
			data = json.dumps(data)
			ws.write_message(data)

			data = {"target": "display6", "value" : r}
			data = json.dumps(data)
			ws.write_message(data)
			
			data = {"target": "display8", "value" : Fence_Actual}
			data = json.dumps(data)
			ws.write_message(data)
			
			data = {"target": "display9", "value" : Height_Actual}
			data = json.dumps(data)
			ws.write_message(data)

class SocketHandler(tornado.websocket.WebSocketHandler):
	def check_origin(self, origin):
		return True

	def open(self):
		global ws
		ws=self
		print "Websocket opened"

	# Gestione dei messaggi in ricezione dal Chromium

	def on_message(self, message):
		#global i
		global Height_Actual
		global Height_Target
		global Fence_Actual
		global Fence_Target

		print message
		data=json.loads(message)

		try:

			# cambia lo stato del pulsante ABS in INCR nella Pagina DRO
			if data["event"]=="click":
				if data["id"]=="abs_incr":
					if data["value"]=="ABS":
						data = {"target": "abs_incr", "value" : "INCR"}
						print "ABS"
					else:
						data = {"target": "abs_incr", "value" : "ABS"}
						print "INCR"

					data = json.dumps(data)
					ws.write_message(data)
					return

			# cambia lo stato del pulsante mm in inch nella Pagina DRO
			if data["event"]=="click":
				if data["id"]=="mm_inch":
					if data["value"]=="MM":
						data = {"target": "mm_inch", "value" : "INCH"}
						print "INCH"
					else:
						data = {"target": "mm_inch", "value" : "MM"}
						print "MM"

					data = json.dumps(data)
					ws.write_message(data)
					return

			if data["event"]=="click":
				if data["id"]=="button_units":
					if data["value"]=="images/mm.jpg":
						data = {"target": "button_units", "value" : "images/inch.jpg"}
						print "Unit inch"
					else:
						data = {"target": "button_units", "value" : "images/mm.jpg"}
						print "Unit mm"

					data = json.dumps(data)
					ws.write_message(data)
					return

			if data["event"]=="click":
				if data["id"]=="button_mode":
					if data["value"]=="images/abs.jpg":
						data = {"target": "button_mode", "value" : "images/inc.jpg"}
						print "Mode inc"
					else:
						data = {"target": "button_mode", "value" : "images/abs.jpg"}
						print "Mode abs"

					data = json.dumps(data)
					ws.write_message(data)
					return

			if data["event"]=="click":
				if data["id"]=="button_zero1":
					if data["value"]=="images/zero1.jpg":
						data = {"target": "button_zero1", "value" : "images/zero1.jpg"}
						print "Fence Zero"
					else:
						data = {"target": "button_zero1", "value" : "images/zero1.jpg"}
						print "Fence Zero"

					data = json.dumps(data)
					ws.write_message(data)
					return

			if data["event"]=="click":
				if data["id"]=="button_zero2":
					if data["value"]=="images/zero2.jpg":
						data = {"target": "button_zero2", "value" : "images/zero2.jpg"}
						print "Height Zero"
					else:
						data = {"target": "button_zero2", "value" : "images/zero2.jpg"}
						print "Height Zero"

					data = json.dumps(data)
					ws.write_message(data)
					return
		

			if data["event"]=="click":
				if data["id"]=="button_zero3":
					if data["value"]=="images/zero3.jpg":
						data = {"target": "button_zero3", "value" : "images/zero3.jpg"}
						print "Angle Zero"
					else:
						data = {"target": "button_zero3", "value" : "images/zero3.jpg"}
						print "Angle Zero"

					data = json.dumps(data)
					ws.write_message(data)
					return

			if data["event"]=="click":
				if data["id"]=="Left":
					if data["value"]=="images/navbuttonLeftON.gif":
						data = {"target": "Left", "value" : "images/navbuttonLeft.gif"}
						print "click"
					else:
						data = {"target": "Left", "value" : "images/navbuttonLeftON.gif"}
						print "clock"

					data = json.dumps(data)
					ws.write_message(data)
					return

			if data["event"]=="click":
				if data["id"]=="Center":
					if data["value"]=="images/navbuttonCenterON.gif":
						data = {"target": "Center", "value" : "images/navbuttonCenter.gif"}
						print "click"
					else:
						data = {"target": "Center", "value" : "images/navbuttonCenterON.gif"}
						print "clock"

					data = json.dumps(data)
					ws.write_message(data)
					return

			if data["event"]=="click":
				if data["id"]=="Right":
					if data["value"]=="images/navbuttonRightON.gif":
						data = {"target": "Right", "value" : "images/navbuttonRight.gif"}
						print "click"
					else:
						data = {"target": "Right", "value" : "images/navbuttonRightON.gif"}
						print "clock"

					data = json.dumps(data)
					ws.write_message(data)
					return

			if data["event"]=="click":
				if data["id"]=="Up":
					if data["value"]=="images/navbuttonUpON.gif":
						data = {"target": "Up", "value" : "images/navbuttonUp.gif"}
						print "click"
					else:
						data = {"target": "Up", "value" : "images/navbuttonUpON.gif"}
						print "clock"

					data = json.dumps(data)
					ws.write_message(data)
					return

			if data["event"]=="click":
				if data["id"]=="Down":
					if data["value"]=="images/navbuttonDownON.gif":
						data = {"target": "Down", "value" : "images/navbuttonDown.gif"}
						print "click"
					else:
						data = {"target": "Down", "value" : "images/navbuttonDownON.gif"}
						print "clock"

					data = json.dumps(data)
					ws.write_message(data)
					return
					
	# ---------------------------------------------------------				
	# -------------------- Motor Actions ----------------------
	# ---------------------------------------------------------
	
			if data["event"]=="setup":
				if data["id"]=="fence":
					#print data["value"]
					Fence_Target = float(data["value"])
					Fence_ABSMove = Fence_Target - Fence_Actual
					Fence_Actual = Fence_Target
#					MoveFence(Fence_ABSMove)
					# drive the motor in a background thread
					x = threading.Thread(target=MoveFence, args=(Fence_ABSMove,))
					x.start()
					return

			if data["event"]=="setup":
				if data["id"]=="height":
					#print data["value"]
					Height_Target = float(data["value"])
					Height_ABSMove = Height_Target - Height_Actual
					Height_Actual = Height_Target
#					MoveHeight(Height_ABSMove)
					# drive the motor in a background thread
					x = threading.Thread(target=MoveHeight, args=(Height_ABSMove,))
					x.start()
					return

			if data["event"]=="setup":
				if data["id"]=="relativeFence":
					print data["value"]
					Fence_RelativeMove = float(data["value"])
					Fence_Actual = Fence_Actual + Fence_RelativeMove
#					MoveFenceRel(Fence_RelativeMove)
					# drive the motor in a background thread
					x = threading.Thread(target=MoveFence, args=(Fence_RelativeMove,))
					x.start()
					return

			if data["event"]=="setup":
				if data["id"]=="relativeHeight":
					print data["value"]
					Height_RelativeMove = float(data["value"])
					Height_Actual = Height_Actual + Height_RelativeMove
#					MoveHeight(Height_RelativeMove)
					# drive the motor in a background thread
					x = threading.Thread(target=MoveHeight, args=(Height_RelativeMove,))
					x.start()					
					return

	
	# ---------------------------------------------------------
	# ------------------ Homing Buttons -----------------------
	# ---------------------------------------------------------
					
			if data["event"]=="click":
				if data["id"]=="height_homing":
					heightHoming()
					return
					
			if data["event"]=="click":
				if data["id"]=="fence_homing":
					fenceHoming()
					return


	# ---------------------------------------------------------	
	# ------------------- Auto Zero ---------------------------
	# ---------------------------------------------------------	
	
			if data["event"]=="click":
				if data["id"]=="height_probe":
					zeroHeight()
					return
					
			if data["event"]=="click":
				if data["id"]=="fence_probe":
					zeroFence()
					return

	# ---------------------------------------------------------	
	# ------------------- Shutdown ----------------------------
	# ---------------------------------------------------------				
					
			if data["event"]=="click":
				if data["id"]=="Shutdown":
					call("sudo systemctl halt", shell=True)
					data = json.dumps(data)
					ws.write_message(data)
					return

			if data["event"]=="click":
				if data["id"]=="Reboot":
					call("sudo systemctl reboot", shell=True)
					data = json.dumps(data)
					ws.write_message(data)
					return

		except Exception, err:
			try:
				exc_info = sys.exc_info()

			finally:
				# Display the *original* exception
				traceback.print_exception(*exc_info)
				del exc_info

	def on_close(self):
		print "Websocket closed"

application = tornado.web.Application([
	(r'/ws', SocketHandler),
	(r"/(.*)", tornado.web.StaticFileHandler, {"path": "../www","default_filename": "index.html"}),
])



try:
	t = threading.Thread(target=counter)
	t.start()

	application.listen(80,"0.0.0.0")
	tornado.ioloop.IOLoop.instance().start()

except:
	print("Unexpected error:", sys.exc_info()[0])
	t_exit=True
	t.join()
