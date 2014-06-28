import thread
from Tkinter import *

class GUI(object):
	def __init__(self, server):
		self.server = server
		thread.start_new_thread(self.startGUI, ())
	def startGUI(self):
			self.window = Tk()
			self.window.title = 'ITorrent'

			
			#add peer section
			entryIP = StringVar()
			def requestToAddPeer(*args):
				try:
					data = entryIP.get().split(':')
					self.server.requestAddPeer(data[0],data[1])
				except:
					pass
				

			
			entryIP_obj = Entry(self.window, textvariable = entryIP)
			entryIP_obj.grid(row = 0,column = 0, sticky=(W))

			Button(self.window, text='add peer', command = requestToAddPeer).grid(row=0,column=1,sticky=(W))

			#find files section
			def downloadFile(*args):
				self.server.requestFile(entryFileName.get())

			entryIP_obj = Entry(self.window, textvariable = entryIP)
			entryIP_obj.grid(row = 1,column = 0, sticky=(W))

			Button(self.window, text='download file', command = downloadFile).grid(row=1,column=1,sticky=(W))

			self.window.mainloop()

