from flask import Flask, request
from  httplib import HTTPConnection
from parser import *

def isAllKeysExist(l, keys):
	for obj in l:
		if not obj in keys:
			return False
	return True 
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
				sendResponses(response, request.remote_addr)		
			return ''
		
		self.app.run(debug = True, host = self.ip, port = self.port)

	def sendResponses(self, responseTuple, sourceIP):
		if sourceIP in peers.keys():
			conn = HTTPConnection(sourceIP+ ':' + peers[sourceIP])
			conn.request('GET','/' + responseTuple[2])
		else: 
			pass #request came from new peer
		if isAllKeysExist(responseTuple[0], self.peers):
			for ip in responseTuple[0]:
				conn = HTTPConnection(ip+ ':' + peers[ip])
				conn.request('GET','/' + responseTuple[1])
		
