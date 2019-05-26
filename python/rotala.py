#!/usr/bin/python

import tornado.ioloop
import tornado.web
import tornado.websocket
import time
import threading
import json
import sys
import smbus
from Stepper import stepper
from subprocess import call

ws=None
t_exit=False
 
I2C_ADDRESS = 0x36

bus = smbus.SMBus(1)

#stepper variables
#[stepPin, directionPin, enablePin]
runHeight = stepper([25, 26, 29])
runFence = stepper([27, 28, 30])

i=0.0 # Fence Display
Height_Actual = 0.0		# Height Display
Height_Target = 0.0

Fence_Actual = 0.0
Fence_Target = 0.0


def MoveFence(ABS):
	if ABS > 0:
		runFence.step(ABS*200, "left"); #steps, dir, speed, stayOn
		runFence.cleanGPIO
	else:
		runFence.step(ABS*200, "right"); #steps, dir, speed, stayOn
		runFence.cleanGPIO


def MoveHeight(ABS):
	if ABS > 0:
		runHeight.step(ABS*200, "left"); #steps, dir, speed, stayOn
		runHeight.cleanGPIO
	else:
		runHeight.step(ABS*200, "right"); #steps, dir, speed, stayOn
		runHeight.cleanGPIO


def counter():
	global i
	global Height_Actual
	global Height_Target
	global Fence_Actual
	global Fence_Target
	
# i, z, r, valori di inizializazione dei display (solo test)
	z=90  # Height Display
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
		#print z
		
		
		
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
			
class SocketHandler(tornado.websocket.WebSocketHandler):
	def check_origin(self, origin):
		return True

	def open(self):
		global ws
		ws=self
		print "Websocket opened"

	# Gestione dei messaggi in ricezione dal Chromium

	def on_message(self, message):
		global i
		global Height_Actual
		global Height_Target
		global Fence_Actual
		global Fence_Target
		
		print message
		data=json.loads(message)

		print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

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
				
		if data["event"]=="setup":
			if data["id"]=="fence":
				#print data["value"]
				Fence_Target = float(data["value"])
				Fence_ABSMove = Fence_Target - Fence_Actual
				Fence_Actual = Fence_Target
				MoveFence(Fence_ABSMove)
				return
				
		if data["event"]=="setup":
			if data["id"]=="height":
				#print data["value"]
				Height_Target = float(data["value"])
				Height_ABSMove = Height_Target - Height_Actual
				Height_Actual = Height_Target
				MoveHeight(Height_ABSMove)
				return
				
		if data["event"]=="setup":
			if data["id"]=="relativeFence":
				print data["value"]			
				Fence_RelativeMove = float(data["value"])
				Fence_Actual = Fence_Actual + Fence_RelativeMove
				MoveFence(Fence_RelativeMove)
				return

		if data["event"]=="setup":
			if data["id"]=="relativeHeight":
				print data["value"]			
				Height_RelativeMove = float(data["value"])
				Height_Actual = Height_Actual + Height_RelativeMove
				MoveHeight(Height_RelativeMove)
				return
		if data["event"]=="click":
			if data["id"]=="Shutdown":
				call("sudo systemctl halt", shell=True)
				data = json.dumps(data)
				ws.write_message(data)
				return
		if data["event"]=="click":
			if data["id"]=="Reboot":
				call("sudo reboot", shell=True)
				data = json.dumps(data)
				ws.write_message(data)
				return	
								
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
