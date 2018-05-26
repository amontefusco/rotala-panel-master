#!/usr/bin/python

import tornado.ioloop
import tornado.web
import tornado.websocket
import time
import threading
import json
import sys

ws=None
t_exit=False
 
def counter():
	i=0
	z=999
	r=450
	while True:
		if t_exit==True:
			print "Bye"
			break
		i=i+1
		z=z-1
		r=r-1
		time.sleep(1)
		print i 

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
		
		if data["event"]=="click":
			if data["id"]=="abs_inc": 
				if data["value"]=="ABS":
					data = {"target": "abs_inc", "value" : "INC"}
					print "ABS"
				else:
					data = {"target": "abs_inc", "value" : "ABS"}
					print "INC"

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
