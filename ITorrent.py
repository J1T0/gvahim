from flaskServer import *
import thread
from GUI import *
def runGUI():
		#setup GUI
		
		window.mainloop()
if __name__ == '__main__':

	server = FlaskPeer('192.168.1.101',5018,'shared')
	GUI(server)
	server.runServer()
