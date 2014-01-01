from flask import Flask
import httplib

class FlaskPeer(object):
	
	
	def __init__(self):
		self.app = Flask(__name__)
		self.peers = []
		self.potocolVer = '0101'

	def m00(self, dat):
		pass
	def m10(self, dat):
		if not dat == self.protocolVer:
			pass
	def m20(self, dat):
		ttl = dat[:2]
		source_addr = dat[2:10]
		port = [10:12]
		numOfDest = int(dat[12:14],16)
		addrs = dat[14:]
		parsedAddrs = []
		parsedPorts = []
		for i in range(numOfDest):
			parsedAddrs.append(addrs[i*8:(i+1)*8])
			parsedPorts.append(addrs[ (numOfDest*8 + i*4) : (numOfDest*8 + (i + 1)*4) ])
		
		
	def m30(self, dat):
		pass
	def m40(self, dat):
		pass
	def m41(self, dat):
		pass
	def runServer(self):
		@self.app.route('/<string:message>')
		def readMassage(message):
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

			return ''
		self.app.run(debug=True)

if __name__=='__main__':
	server=FlaskPeer()
	server.runServer()
