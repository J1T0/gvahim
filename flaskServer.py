from flask import Flask
from  httplib import HTTPConnection
from parser import *

class FlaskPeer(object):
	def __init__(self,ip,port):
		self.ip = ip
		self.port = port
		self.app = Flask(__name__)
		self.peers = {}
		self.parser = Parser()

	def runServer(self):
		
		@self.app.route('/<string:message>')
		def readMessage(message):
			for response in self.parser.parseMessage(message):
				sendResponses(response)		
			return ''
		
		self.app.run(debug = True, host = self.ip, port = self.port)

	def sendResponses(self, responseTuple, sourceIP):
		pass
		
