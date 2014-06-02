class ProtocolError(Exception):
	def __str__(self):
		return repr('Bad protocol message')
class Parser(object):
	def __init__(self, ip, port):
		self.dests = {}
		self.forwardMessage = ''
		self.responseMessage = ''
		self.ip = ip
		self.port = port
		self.protocolVer = '0001'

	def m00(self, dat):
		pass
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
		ttl = int(dat[:2],16) - 1
		sourceAddr = dat[2:10]
		port = dat[10:14]
		numOfDest = int(dat[14:16],16)
		addrs = dat[16:]
		if numOfDest * 12 != len(addrs):
			raise ProtocolError()
		dests={}
		for i in range(numOfDest):
			parsedAddr = addrs[i*8:(i+1)*8]
			parsedPort = addrs[ (numOfDest*8 + i*4) : (numOfDest*8 + (i + 1)*4) ]
			dests[parsedAddr] = parsedPort
		self.sourceAddr = sourceAddr
		self.dests = dests
				
		
	def m30(self, dat):
		pass
	def m40(self, dat):
		pass
	def m41(self, dat):
		pass	
	
	def parseMessage(message):
		self.dests = {}
		while len(message)>5:
			try:
				key = message[:2]
				if not key in ['40']: # 40 massage has 2 byte long length param.
					data = message[4:(int(message[2:4],16)*2 +4)]
					if key in ['00' , '10', '20', '30', '41']: # protocol error
						raise ProtocolError()
					if key == '00':
						m00(data)
					elif key == '10':
						m10(data)
					elif key == '20':
						if not dests == {}:
							yield self.dests, self.forwardMessage, self.responseMessage
	  						self.dests = {}
							self.forwardMessage = ''
							self.responseMessage = ''
						m20(data)
					elif key == '30':
						m30(data)
					elif key == '41':
						m41(data)
					message = message[(int(message[2:4],16)*2 +4):]
					continue
				data = message[6:(int(message[2:6],16)*2 +6)]
				m40(data)
				message = message[(int(message[2:6],16)*2 +6):]
				yield self.dests, self.forwardMessage, self.responseMessage  
			except:
				yield {}, '', '000101'

