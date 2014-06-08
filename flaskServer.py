from flask import Flask, request
from  httplib import HTTPConnection
from parser import *

class NoFreeSpotsInServerException(Exception):
	def __str__(self):
		return repr('no free spaces in the client')

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
		self.parser = Parser(self)
		self.MAX_PEERS = 5
		self.joinRequestQueue = []
		self.conn = HTTPConnection('')
	
	def requestAddPeer(self,ip,port):
		hexIp = self.parser.parseIPToHexStr(ip)
		hexPort = self.parser.parsePortToHexStr(port)
		self.joinRequestQueue.append((hexIp,hexPort))
		request = self.parser.parseJoinRequest(ip, port)
		self.conn = HTTPConnection(ip+ ':' + port)
		self.conn.request('GET','/' + request)

	def addPeer(self,ip, port):
		if len(self.peers) == self.MAX_PEERS:
			raise NoFreeSpotsInServerException()
		self.peers[ip] = port
		print 'peers: '+ str(self.peers)
		
	def runServer(self):
		
		@self.app.route('/<string:message>')
		def readMessage(message):
			#try:
			for response in self.parser.parseMessage(message):
				self.sendResponses(response, request.remote_addr)
			#except Exception as e:
			#	print 'readMessage' + str(e)
			return ''
		
		self.app.run( host = self.ip, port = self.port)

	def sendResponses(self, responseTuple, sourceIP):
		print 'a'
		parsedSourceIP = self.parser.parseIPToHexStr(sourceIP)
		m20 = self.parser.parseResponseM20(parsedSourceIP,self.peers[parsedSourceIP])
		print 'b'
		decPort = str(int(self.peers[parsedSourceIP],16))
		if parsedSourceIP in self.peers.keys():
			if responseTuple[2] != '':
				responseMessage = m20+responseTuple[2]
				print 'sending response: ' + responseMessage 
				self.conn = HTTPConnection(sourceIP+ ':' + decPort)
				self.conn.request('GET','/' + responseMessage)
		if responseTuple[1] != '':
			if isAllKeysExist(responseTuple[0], self.peers):
				for ip in responseTuple[0]:
					responseMessage = m20+responseTuple[1] 
					self.conn = HTTPConnection(ip+ ':' + self.peers[ip])
					self.conn.request('GET','/' + responseMessage)
			
