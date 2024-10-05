# from kivy.config import Config
WIDTH  = int(750  * 0.5) 
HEIGHT = int(1400 * 0.5) 
# Config.set('graphics', 'width', WIDTH)
# Config.set('graphics', 'height', HEIGHT)
# Config.set('graphics', 'resizable', 0)
# Config.write()

from kivy.utils import platform
from kivy.core.window import Window

if platform == "win":
	Window.size  = (WIDTH, HEIGHT)
	Window.top   = 30
	Window.left  = 1

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from theme import OriginalColor

DEVELOPMENT = False

class Login(Screen):

	def open_signup(self):
		self.manager.transition = SlideTransition(direction="left")
		self.manager.current = "register"

class Register(Screen):

	def open_login(self):
		self.manager.transition = SlideTransition(direction="right")
		self.manager.current = "login"

class Manager(ScreenManager):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.theme = OriginalColor()

		self.url_link = "http://localhost:8888"
		if not DEVELOPMENT:
			self.url_link = "https://test888.netlify.app"


class APSApp(App):
	def build(self):
		return Manager()

if __name__ == '__main__':
	APSApp().run()
