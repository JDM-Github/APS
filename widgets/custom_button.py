from kivy.uix.label import Label
from kivy.uix.widget import Widget

from kivy.metrics import dp
from kivy.utils import get_color_from_hex as GetColor
from kivy.graphics import RoundedRectangle, Color

class CustomButton(Widget):

	def __init__(self, root, text='', on_press=lambda: None, **kwargs):
		super().__init__(**kwargs)
		self.root = root
		self.on_press = on_press
		self.tdown     = False

		self.size_hint = (0.8, None)
		self.height    = dp(45)
		self.pos_hint  = {"center_x": 0.5}

		self.label = Label(text=text, bold=True)
		self.add_widget(self.label)

		with self.canvas.before:
			self.color = Color(rgba=GetColor(self.root.theme.main_color))
			self.rounded_rect = RoundedRectangle(pos=(self.pos), size=self.size, radius=[dp(20)])

		self.bind(pos=self.update_rect, size=self.update_rect)

	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			self.tdown = True
			self.color.rgba = GetColor(self.root.theme.main_hover_color)

	def on_touch_up(self, touch):
		if self.tdown:
			self.tdown = False
			self.color.rgba = GetColor(self.root.theme.main_color)
			if self.collide_point(*touch.pos):
				self.on_press()

	def update_rect(self, *args):
		self.rounded_rect.pos  = self.pos
		self.rounded_rect.size = self.size

		self.label.size = self.size
		self.label.pos = self.pos