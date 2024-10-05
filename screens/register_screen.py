import re
import json
import requests
import threading
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock

from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex as GetColor
from kivy.graphics import Rectangle, RoundedRectangle, Color, Line, Ellipse
from kivy.uix.screenmanager import SlideTransition, FadeTransition, WipeTransition, SwapTransition

from widgets import RoundedTextInput, CustomButton, LoadingPopup, BackButton

class TermsAgreement(Widget):

	def __init__(self, root, **kwargs):
		super().__init__(**kwargs)
		self.size_hint_x = 0.7
		self.size_hint_y = None
		self.height = dp(40)
		self.pos_hint = {"center_x": 0.5}

		self.layout = BoxLayout(orientation='horizontal')
		self.checkbox = CheckBox(size_hint=(None, 1), width=dp(20))
		terms_policy_label = Label(
			font_size=sp(14),
			text="I agree to the [ref=terms][b]Terms[/b][/ref] and [ref=policy][b]Policy[/b][/ref].",
			markup=True,
			color=GetColor(root.theme.main_color)
		)
		self.layout.add_widget(self.checkbox)
		self.layout.add_widget(terms_policy_label)

		self.add_widget(self.layout)
		self.bind(pos=self.update_pos, size=self.update_pos)

	def update_pos(self, *_):
		self.layout.pos  = self.pos
		self.layout.size = self.size

class RegisterScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def display_design(self):
		self.size = self.manager.size
		with self.canvas.before:
			Color(rgba=GetColor("#ffffff"))
			Rectangle(size=self.size)

			Color(rgba=GetColor(self.manager.theme.main_color))
			RoundedRectangle(pos=(self.x, self.height-dp(250)), size=(self.width, dp(250)), radius=[0, 0, dp(30), dp(30)])

		self.display_widget()

	def display_widget(self):
		self.clear_widgets()

		widget = Widget(size=self.manager.size, pos=(0, 0))
		layout = BoxLayout(size=self.manager.size, orientation='vertical', padding=dp(10), spacing=dp(10))

		main_color     = self.manager.theme.main_color
		main_color_88  = self.manager.theme.main_color_88
		self.username  = RoundedTextInput(icon_source='assets/user.png', line_color=main_color, fg_color=main_color, hint_color=main_color_88, hint_text="Username")
		self.email     = RoundedTextInput(icon_source='assets/email.png', line_color=main_color, fg_color=main_color, hint_color=main_color_88, hint_text="Email")
		self.password  = RoundedTextInput(icon_source='assets/pass.png', line_color=main_color, fg_color=main_color,
			eye_icon_source='assets/close.png', hint_color=main_color_88, hint_text="Password", password=True)
		self.cpassword = RoundedTextInput(icon_source='assets/pass.png', line_color=main_color, fg_color=main_color,
			eye_icon_source='assets/close.png', hint_color=main_color_88, hint_text="Confirm Password", password=True)
		
		register_btn      = CustomButton(self.manager, text="Sign Up", on_press=self.register)

		layout.add_widget(self.username)
		layout.add_widget(self.email)
		layout.add_widget(self.password)
		layout.add_widget(self.cpassword)

		layout.add_widget(Widget(size_hint_y=None, height=dp(10)))
		layout.add_widget(TermsAgreement(self.manager))
		layout.add_widget(register_btn)

		layout.add_widget(Widget(size_hint_y=None, height=dp(10)))
		ref_login = Label(color=GetColor(self.manager.theme.main_color),
			font_size=sp(14),
			text="Have an account? [ref=login][b]Sign in[/b][/ref]",
			markup=True, size_hint_y=None, height=dp(20))
		ref_login.bind(on_ref_press=self.layout_on_ref_press)

		layout.add_widget(ref_login)
		layout.add_widget(Widget(size_hint_y=None, height=dp(10)))

		widget.add_widget(layout)
		self.back_button = BackButton(self.manager, on_press=self.go_to_login)
		widget.add_widget(self.back_button)
		self.add_widget(widget)

	def layout_on_ref_press(self, *args):
		if args[1] == "login":
			self.go_to_login()

	def is_strong_password(self, password):
		if len(password) < 8:
			return False
		if not re.search(r'[A-Z]', password):  # At least one uppercase letter
			return False
		if not re.search(r'[a-z]', password):  # At least one lowercase letter
			return False
		if not re.search(r'[0-9]', password):  # At least one digit
			return False
		if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):  # At least one special character
			return False
		return True

	def register(self):
		self.loading = LoadingPopup(self.manager)
		self.add_widget(self.loading)

		self.username.color.rgba  = GetColor(self.manager.theme.main_color)
		self.email.color.rgba     = GetColor(self.manager.theme.main_color)
		self.password.color.rgba  = GetColor(self.manager.theme.main_color)
		self.cpassword.color.rgba = GetColor(self.manager.theme.main_color)

		# Validate username
		if self.username.input.text.strip() == "":
			self.username.color.rgba = GetColor(self.manager.theme.main_error_color)
			self._on_error('', "Username cannot be empty. Please enter a valid username.")
			return

		email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
		if self.email.input.text.strip() == "":
			self.email.color.rgba = GetColor(self.manager.theme.main_error_color)
			self._on_error('', "Email cannot be empty. Please enter a valid email address.")
			return
		elif not re.match(email_pattern, self.email.input.text.strip()):
			self.email.color.rgba = GetColor(self.manager.theme.main_error_color)
			self._on_error('', "Invalid email format. Please enter a valid email address.")
			return

		# Validate password
		if self.password.input.text.strip() == "":
			self.password.color.rgba = GetColor(self.manager.theme.main_error_color)
			self._on_error('', "Password cannot be empty. Please enter a valid password.")
			return
		elif not self.is_strong_password(self.password.input.text):
			self.password.color.rgba = GetColor(self.manager.theme.main_error_color)
			self._on_error('', "Password is too weak. It must be at least 8 characters long, include a mix of uppercase and lowercase letters, numbers, and special characters.")
			return

		# Validate confirm password
		if self.cpassword.input.text.strip() == "":
			self.cpassword.color.rgba = GetColor(self.manager.theme.main_error_color)
			self._on_error('', "Please confirm your password.")
			return

		# Check if passwords match
		if self.password.input.text != self.cpassword.input.text:
			self.password.color.rgba  = GetColor(self.manager.theme.main_error_color)
			self.cpassword.color.rgba = GetColor(self.manager.theme.main_error_color)
			self._on_error('', "Passwords do not match. Please ensure both passwords are identical.")
			return

		threading.Thread(target=self._register).start()

	def on_success(self, result):
		Clock.schedule_once(lambda dt: self._on_success(result))

	def on_error(self, error):
		Clock.schedule_once(lambda dt: self._on_error(error))

	def show_error_popup(self, message):
		popup = Popup(title='Register Failed',
					  content=Label(text=message),
					  size_hint=(0.8, 0.4))

		popup.open()

	def go_to_login(self):
		self.manager.transition = SlideTransition(direction='right', duration=0.5)
		self.manager.current = 'login'

	def _register(self):
		data = {
			'username': self.username.input.text,
			'email'   : self.email.input.text,
			'password': self.password.input.text
		}
		try:
			response = requests.post(
				f'{self.manager.url_link}/.netlify/functions/api/register',
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
		self.manager.get_screen('verify').to_verify = result['otp']
		self.manager.current = 'verify'

	def _on_error(self, error, error_message="Error occurred while processing the request."):
		self.remove_widget(self.loading)
		print(f"Error: {error}")
		self.show_error_popup(error_message)
