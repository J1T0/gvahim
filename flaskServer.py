from flask import Flask, request
from  httplib import HTTPConnection
from parser import *
import os

class NoFreeSpotsInServerException(Exception):
	def __str__(self):
		return repr('no free spaces in the client')

def isAllKeysExist(l, keys):
	for obj in l:
		if not obj in keys:
			return False
	return True 
class FlaskPeer(object):
	def __init__(self,ip,port,sharedDir):
		self.ip = ip
		self.port = port
		self.app = Flask(__name__)
		self.peers = {}
		self.parser = Parser(self)
		self.MAX_PEERS = 5
		self.joinRequestQueue = []
		self.fileRequestQueue = []
		self.conn = HTTPConnection('')
		self.sharedDir = sharedDir
	
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
		
	def requestFile(self, fileName):
		self.fileRequestQueue.append(fileName)
		self.hexFileName = ''.join([hex(ord(i)).split('x')[1] for i in fileName]).upper()
		request = self.parser.parseFileRequest(self.hexFileName)
		for ip in self.peers:
			decIp = '.'.join([str(int(ip[i*2]+ip[i*2+1],16)) for i in xrange(4)])
			decPort = int(self.peers[ip],16)
			self.conn = HTTPConnection(decIp+ ':' + str(decPort))
			self.conn.request('GET','/' + request)

	def getFileBytes(self,fileName):
		for f in os.listdir(self.sharedDir):
			if ''.join([hex(ord(i)).split('x')[1] for i in f]).upper() == fileName:
				with open(self.sharedDir+'/' + f) as fi:
					return ''.join([hex(ord(i)).split('x')[1] for i in fi.read()]).upper()

	def saveFile(self, data):
		print 'saveFile'+data
		with open(self.sharedDir +'/' + self.fileRequestQueue[0],'w+') as f:
			print 'edited data ' + ''.join([chr(int(data[i*2]+data[i*2+1],16)) for i in xrange(len(data)/2)])
			f.write(''.join([chr(int(data[i*2]+data[i*2+1],16)) for i in xrange(len(data)/2)]))
	
	def runServer(self):
		
		@self.app.route('/<string:message>')
		def readMessage(message):
			try:
				for response in self.parser.parseMessage(message):
					self.sendResponses(response, request.remote_addr)
			except Exception as e:
				print 'readMessage' + str(e)
			return ''
		
		self.app.run( host = self.ip, port = self.port)

	def sendResponses(self, responseTuple, sourceIP):
		parsedSourceIP = self.parser.parseIPToHexStr(sourceIP)
		m20 = self.parser.parseResponseM20(parsedSourceIP,self.peers[parsedSourceIP])
		decPort = str(int(self.peers[parsedSourceIP],16))
		if parsedSourceIP in self.peers.keys():
			if responseTuple[2] != '':
				responseMessage = m20+responseTuple[2]
				self.conn = HTTPConnection(sourceIP+ ':' + decPort)
				self.conn.request('GET','/' + responseMessage)
		if responseTuple[1] != '':
			if isAllKeysExist(responseTuple[0], self.peers):
				for ip in responseTuple[0]:
					responseMessage = m20+responseTuple[1] 
					self.conn = HTTPConnection(ip+ ':' + self.peers[ip])
					self.conn.request('GET','/' + responseMessage)
			
