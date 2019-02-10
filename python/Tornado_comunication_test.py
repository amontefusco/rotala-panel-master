import tornado.ioloop
import tornado.web
import tornado.websocket
import time
import threading

ws=None

def counter():
	i=0
	while True:
		i=i+1
		print i
		time.sleep(0.1)
		if ws<>None:
			ws.write_message("%d" % i)

class SocketHandler(tornado.websocket.WebSocketHandler):
	def check_origin(self, origin):
		return True

	def open(self):
		global ws
		ws=self
		print "Websocket opened"

	def on_message(self, message):
		print(u"You said: " + message)
		self.write_message(u"You said: " + message)

	def on_close(self):
		print "Websocket closed"

application = tornado.web.Application([
	(r'/ws', SocketHandler),
	(r"/(.*)", tornado.web.StaticFileHandler, {"path": "../www","default_filename": "index.html"}),
])

if __name__ == "__main__":
	t = threading.Thread(target=counter)
	t.start()

	application.listen(80,"0.0.0.0")
	tornado.ioloop.IOLoop.instance().start()