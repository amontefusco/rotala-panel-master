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

ws=None
t_exit=False
 
I2C_ADDRESS = 0x36

bus = smbus.SMBus(1)
 
def counter():

# i, z, r, valori di inizializazione dei display
	i=0.1 # Fence Display
	z=90  # Height Display
	r=45  # Angle Display (used only for test purpose)
	
	while True:

#	I2c angle position sensor initialization. (commentato in fase di test quando il sensore non è connesso) 
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
		i = i + 0.1
		if z > 0.01:
			z -= 0.1
		#r=angolo/8  # divide 360 angle to display 45 deg commentato quando manca il sensore
		time.sleep(0.1)
		print z
# comunica i valori dei display al pannello.
		if ws<>None:
			data = {"target": "display1", "value" : i}
			data = json.dumps(data)
			ws.write_message(data)

			data = {"target": "display2", "value" : z}
			data = json.dumps(data)
			ws.write_message(data)
			
			data = {"target": "display3", "value" : r}
			data = json.dumps(data)
			ws.write_message(data)
			
			data = {"target": "display4", "value" : i}
			data = json.dumps(data)
			ws.write_message(data)

			data = {"target": "display5", "value" : z}
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
		#print message
		data=json.loads(message)
		
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
				
		if data["event"]=="change":
			if data["id"]=="zSpeed": 
				print "xxxxxxxxxxxxxxxxxxxxxx"
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
