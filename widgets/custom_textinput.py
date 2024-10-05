from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.widget import Widget

from kivy.metrics import dp
from kivy.utils import get_color_from_hex as GetColor
from kivy.graphics import Color, Line

class RoundedTextInput(Widget):

	def __init__(self,
		icon_source='',
		eye_icon_source='',
		hint_text='',
		password=False,
		line_color="#ffffff88",
		fg_color="#ffffff",
		hint_color="#ffffff88",
		**kwargs):
		super().__init__(**kwargs)
		self.size_hint = (0.8, None)
		self.height    = dp(40)
		self.pos_hint  = {"center_x": 0.5}

		self.input = TextInput(
			hint_text=hint_text,
			font_size="12sp",
			multiline=False,
			password=password,
			padding=(dp(20), 0),
			background_color=(0, 0, 0, 0),
			pos_hint = {"center_y": 0.5},
			hint_text_color=GetColor(hint_color),
			foreground_color=GetColor(fg_color),
			cursor_color=GetColor(fg_color)
		)
		self.add_widget(self.input)

		left_padding  = dp(20)
		right_padding = dp(20)
		if icon_source:
			self.icon = Image(source=icon_source, color=fg_color)
			self.icon.size_hint = (None, None)
			self.icon.size = (dp(20), dp(20))
			self.icon.pos_hint = {"center_y": 0.5}
			self.add_widget(self.icon)
			left_padding = dp(40)

		if eye_icon_source:
			self.eye_icon = Image(source=eye_icon_source, color=fg_color)
			self.eye_icon.size_hint = (None, None)
			self.eye_icon.size = (dp(20), dp(20))
			self.eye_icon.pos_hint = {"center_y": 0.5}
			self.add_widget(self.eye_icon)
			right_padding = dp(40)


		self.input.padding = [left_padding, 0, right_padding, 0]

		with self.canvas.before:
			self.color = Color(rgba=GetColor(line_color))
			self.rounded_rect = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(20)), width=dp(1.2))

		self.bind(pos=self.update_rect, size=self.update_rect)

	def on_touch_down(self, touch):
		if (self.collide_point(*touch.pos)
			and hasattr(self, 'eye_icon')
			and self.eye_icon.collide_point(*touch.pos)):
			if self.eye_icon.source == "assets/close.png":
				self.eye_icon.source = "assets/show.png"
				self.input.password = False
			else:
				self.eye_icon.source = "assets/close.png"
				self.input.password = True
		
		return super().on_touch_down(touch)

	def update_rect(self, *args):
		self.rounded_rect.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(20))

		self.input.size = self.size
		self.input.pos = self.x, self.y-dp(10)

		if hasattr(self, 'icon'):
			self.icon.pos = (self.x + dp(10), self.y + (self.height - self.icon.height) / 2)

		if hasattr(self, 'eye_icon'):
			self.eye_icon.pos = (self.x + self.width - dp(30), self.y + (self.height - self.eye_icon.height) / 2)

