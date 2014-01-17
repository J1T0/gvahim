class Parser(object):
	def __init__(self):
		self.dests = {}
		self.forwardMessage = ''
		self.responseMessage = ''

	def m00(self, dat):
		pass
	def m10(self, dat):
		if self.ip in self.dests:
			if not dat == self.protocolVer:
				pass
	def m20(self, dat):
		ttl = dat[:2]
		self.sourceAddr = dat[2:10]
		port = [10:12]
		numOfDest = int(dat[12:14],16)
		addrs = dat[14:]
		for i in range(numOfDest):
			parsedAddr= addrs[i*8:(i+1)*8]
			parsedPort =addrs[ (numOfDest*8 + i*4) : (numOfDest*8 + (i + 1)*4) ]
			self.dests[parsedAddr] = parsedPort
		
	def m30(self, dat):
		pass
	def m40(self, dat):
		pass
	def m41(self, dat):
		pass	
	
	
	def parseMessage(message):
		self.dests = {}
		while len(message)>5:
			key = message[:2]
			if not key in ['40']: # 40 massage has 2 byte long length param.
				data = message[4:(int(message[2:4],16)*2 +4)]
				if key in ['00' , '10', '20', '30', '41']: # protocol error
					return ''
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

