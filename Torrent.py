from flaskServer import *
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

class Window(BoxLayout):
	def __init__(self, title):
		super(Window,self).__init__()


class ConnectionWindowBase(Widget):
	def __init__(self):
		super(ConnectionWindowBase,self).__init__()
	def connect(self):
		self.parent.parent.remove_widget(self.parent)

class ConnectionWindow(BoxLayout):
	def __init__(self):
		super(ConnectionWindow,self).__init__()
		#self.add_widget(ConnectionWindowBase())
		#self.add_widget(Window('bla'))
		

class MainScreen(Widget):
	def __init__(self):
		self.connectionWindow = ConnectionWindow()
		super(MainScreen,self).__init__()
	def show_connect_window(self):
		try:
			self.add_widget(self.connectionWindow)
		except:
			pass

class TorrentApp(App):
	def build(self):
		window = MainScreen()
		return window

if __name__=='__main__':
	TorrentApp().run()
