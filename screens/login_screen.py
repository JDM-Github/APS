import json
import requests
import threading
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.clock import Clock

from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex as GetColor
from kivy.graphics import Rectangle, RoundedRectangle, Color, Line, Ellipse
from kivy.uix.screenmanager import SlideTransition, FadeTransition, WipeTransition, SwapTransition

from widgets import RoundedTextInput, CustomButton, LoadingPopup, BackButton

class CircleImage(Widget):

	def __init__(self, source='',  **kwargs):
		super().__init__(**kwargs)
		self.image = Image(source=source)
		with self.canvas.before:
			self.image_circle = Ellipse(texture=self.image.texture, size=self.size, pos=self.pos)

		self.bind(pos=self.update_rect, size=self.update_rect)

	def update_rect(self, *args):
		self.image_circle.pos  = self.pos
		self.image_circle.size = self.size



class LoginScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def display_design(self):
		self.size = self.manager.size
		with self.canvas.before:
			Color(rgba=GetColor(self.manager.theme.main_color))
			Rectangle(size=self.size)

			Color(rgba=GetColor("#ffffff"))
			RoundedRectangle(size=(self.width, dp(190)), radius=[dp(30), dp(30), 0, 0])

		self.display_widget()

	def display_widget(self):
		self.clear_widgets()

		widget = Widget(size=self.manager.size, pos=(0, 0))

		layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20), size=self.manager.size)
		self.logo = CircleImage(source='assets/JDMBG.png', size_hint=(None, None), pos_hint={"center_x": 0.5}, size=(self.width * 0.65, self.width * 0.65))
		layout.add_widget(self.logo)

		self.username = RoundedTextInput(hint_text="Username", icon_source='assets/user.png')
		self.password = RoundedTextInput(hint_text="Password", password=True,
			icon_source='assets/pass.png',
			eye_icon_source='assets/close.png')

		login_btn = CustomButton(self.manager, text="Login", on_press=self.login)
		register_btn = CustomButton(self.manager, text="Create an account", on_press=self.go_to_register)

		layout.add_widget(Label(text="Japan", font_size=sp(56), bold=True, size_hint_y=None, height=dp(20)))
		layout.add_widget(Widget(size_hint_y=None, height=dp(10)))

		layout.add_widget(self.username)
		layout.add_widget(self.password)
		layout.add_widget(Widget(size_hint_y=None, height=dp(20)))

		layout.add_widget(login_btn)
		layout.add_widget(register_btn)
		layout.add_widget(Widget(size_hint_y=None, height=dp(5)))

		widget.add_widget(layout)
		self.back_button = BackButton(self.manager, on_press=self.go_to_register)
		widget.add_widget(self.back_button)
		self.add_widget(widget)

	def login(self):
		self.loading = LoadingPopup(self.manager)
		self.add_widget(self.loading)

		threading.Thread(target=self._login).start()

	def on_success(self, result):
		Clock.schedule_once(lambda dt: self._on_success(result))

	def on_error(self, error):
		Clock.schedule_once(lambda dt: self._on_error(error))

	def go_to_register(self):
		self.manager.transition = SlideTransition(direction='left', duration=0.5)
		self.manager.current = 'register'

	def show_error_popup(self, message):
		popup = Popup(title='Login Failed',
					  content=Label(text=message),
					  size_hint=(0.8, 0.4))
		popup.open()

	def _login(self):
		data = {
			'username': self.username.input.text,
			'password': self.password.input.text
		}
		try:
			response = requests.post(
				f'{self.manager.url_link}/.netlify/functions/api/login',
				headers={'Content-Type': 'application/json'},
				data=json.dumps(data)
			)
			response.raise_for_status()
			result = response.json()
			self.on_success(result)
		except requests.RequestException as e:
			self.on_error(e)

	def _on_success(self, result):
		self.remove_widget(self.loading)
		if result.get('success'):
			self.manager.current = 'success'
		else:
			self.show_error_popup(result.get('message', 'Login failed.'))

	def _on_error(self, error, error_message="Error occurred while processing the request."):
		self.remove_widget(self.loading)
		print(f"Error: {error}")
		self.show_error_popup(error_message)

	
