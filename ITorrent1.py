from Tkinter import *
from flaskServer import *
import thread
def runGUI():
		#setup GUI
		window = Tk()
		window.title = 'ITorrent'

		
		#add peer section
		entryIP = StringVar()
		def requestToAddPeer(*args):
			try:
				data = entryIP.get().split(':')
				server.requestAddPeer(data[0],data[1])
			except:
				pass
			

		
		entryIP_obj = Entry(window, textvariable = entryIP)
		entryIP_obj.grid(row = 0,column = 0, sticky=(W))

		Button(window, text='add peer', command = requestToAddPeer).grid(row=0,column=1,sticky=(W))

		#find files section
		entryFileName = StringVar()
		def downloadFile(*args):
			server.requestFile(entryFileName.get())

		entryFileName_obj = Entry(window, textvariable = entryFileName)
		entryFileName_obj.grid(row = 1,column = 0, sticky=(W))

		Button(window, text='download file', command = downloadFile).grid(row=1,column=1,sticky=(W))

		window.mainloop()
if __name__ == '__main__':

	server = FlaskPeer('192.168.1.104',5014,'shared1')
	
	thread.start_new_thread(runGUI,())
	server.runServer()
