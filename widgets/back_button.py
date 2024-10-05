from kivy.uix.label import Label
from kivy.uix.widget import Widget

from kivy.metrics import dp
from kivy.utils import get_color_from_hex as GetColor
from kivy.graphics import RoundedRectangle, Color

class BackButton(Widget):

	def __init__(self, root, text='', on_press=lambda: None, **kwargs):
		super().__init__(**kwargs)
		self.root = root
		self.on_press = on_press
		self.tdown     = False

		self.pos = dp(15), root.height - dp(25)
		self.size = (dp(20), dp(20))

		self.label = Label(size=self.size, pos=self.pos, text="Back", bold=True, font_size="16sp")
		self.add_widget(self.label)

	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			self.tdown = True
			self.label.color = "#888888"

	def on_touch_up(self, touch):
		if self.tdown:
			self.tdown = False
			self.label.color = "#ffffff"
			if self.collide_point(*touch.pos):
				self.on_press()
