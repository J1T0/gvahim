class ProtocolError(Exception):
	def __str__(self):
		return repr('Bad protocol message')
class Parser(object):
	def __init__(self, peer):
		self.dests = {}
		self.forwardMessage = ''
		self.responseMessage = ''
		self.ip = peer.ip
		self.port = peer.port
		self.protocolVer = '0001'
		self.peer = peer

	def parseIPToHexStr(self, ip):
		parsedIP = ''
		unparsedBytes = ip.split('.')
		for byte in unparsedBytes:
			if int(byte)/16 < 10:
				parsedIP += str(int(byte)/16)
			else:
				parsedIP += ['A','B','C','D','E','F'][int(byte)/16 - 10]
			if int(byte)%16 < 10:
				parsedIP += str(int(byte)%16)
			else:
				parsedIP += ['A','B','C','D','E','F'][int(byte)%16 - 10]
		return parsedIP

	def parsePortToHexStr(self, port):
		parsedPort = ''
		unparsedBytes = [int(port)/256,int(port) % 256]
		for byte in unparsedBytes:
			if int(byte)/16 < 10:
				parsedPort += str(int(byte)/16)
			else:
				parsedPort += ['A','B','C','D','E','F'][int(byte)/16 - 10]
			if int(byte)%16 < 10:
				parsedPort += str(int(byte)%16)
			else:
				parsedPort += ['A','B','C','D','E','F'][int(byte)%16 - 10]
		return parsedPort

	def m00(self, dat):
		print 'in 00'
		print self.peer.joinRequestQueue
		for i in xrange(len(self.peer.joinRequestQueue)):
			if self.peer.joinRequestQueue[i][0] == self.sourceAddr and self.peer.joinRequestQueue[i][1] == self.sourcePort:
				print dat
				if dat == '00':
					self.peer.addPeer(self.peer.joinRequestQueue[i][0], self.peer.joinRequestQueue[i][1])
				del self.peer.joinRequestQueue[i]
				return
	def m10(self, dat):
		if self.ip in self.dests and self.dests[self.ip] == self.port:
			if not dat == self.protocolVer:
				self.responseMessage += '000101'
			else:
				self.responseMessage += '000100'
			if len(self.dests)>1:
				self.forwardMessage += '1002' + dat
			return
		self.forwardMessage += '1002' + dat
		
	def m20(self, dat):
		self.ttl = int(dat[:2],16) - 1
		self.sourceAddr = dat[2:10]
		self.sourcePort = dat[10:14]
		numOfDest = int(dat[14:16],16)
		addrs = dat[16:]
		if numOfDest * 12 != len(addrs):
			raise ProtocolError()
		dests={}
		for i in range(numOfDest):
			parsedAddr = addrs[i*8:(i+1)*8]
			parsedPort = addrs[ (numOfDest*8 + i*4) : (numOfDest*8 + (i + 1)*4) ]
			dests[parsedAddr] = parsedPort
		self.dests = dests

		if self.parseIPToHexStr(self.ip) in self.dests:
			del self.dests[self.parseIPToHexStr(self.ip)]
		
	def m30(self, dat):
		try:
			self.peer.addPeer(self.sourceAddr, self.sourcePort)
			self.responseMessage += '000100'
		except:
			print 'm30'+str(e)
			self.responseMessage += '000101'
	def m40(self, dat):
		pass
	def m41(self, dat):
		pass	
	
	def parseJoinRequest(self,ip,port):
		parsedIP = self.parseIPToHexStr(ip)
		parsedPort = self.parsePortToHexStr(port)
		out = '200E'
		out += 'FF'
		out += self.parseIPToHexStr(self.ip)
		out += self.parsePortToHexStr(self.port)
		out += '01'
		out += str(parsedIP)
		out += str(parsedPort)
		out += '300100'
		return  out
	def parseResponseM20(self,ip,port):
		response = '200E'
		response += 'FF'
		response += self.parseIPToHexStr(self.ip)
		response += self.parsePortToHexStr(self.port)
		response += '01'
		response += ip
		response += port
		return response
	def parseMessage(self, message):
		self.dests = {}
		while len(message)>5:
			try:
				key = message[:2]
				if not key in ['40']: # 40 massage has 2 byte long length param.
					data = message[4:(int(message[2:4],16)*2 +4)]
					if key not in ['00' , '10', '20', '30', '41']: # protocol error
						raise ProtocolError()
					if key == '00':
						self.m00(data)
					elif key == '10':
						self.m10(data)
					elif key == '20':
						if not self.dests == {}:
							yield self.dests, self.forwardMessage, self.responseMessage
	  						self.dests = {}
							self.forwardMessage = ''
							self.responseMessage = ''
						self.m20(data)
					elif key == '30':
						self.m30(data)
					elif key == '41':
						self.m41(data)
					message = message[(int(message[2:4],16)*2 +4):]
					continue
				data = message[6:(int(message[2:6],16)*2 +6)]
				self.m40(data)
				message = message[(int(message[2:6],16)*2 +6):]  
			except Exception as e:
				print 'main loop'+str(e)
				message = ''
				yield {}, '', '000101'
		yield self.dests, self.forwardMessage, self.responseMessage

