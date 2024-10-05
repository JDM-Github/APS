from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class VerificationScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.to_verify = ""

		layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
		self.label = Label(text="Enter Verification Code")
		layout.add_widget(self.label)

		self.code_input = TextInput(multiline=False, halign='center', font_size=32)
		layout.add_widget(self.code_input)

		self.verify_button = Button(text="Verify Code", on_press=self.verify_code)
		layout.add_widget(self.verify_button)

		self.add_widget(layout)

	def display_design(self):
		pass

	def verify_code(self, instance):
		if self.code_input.text == self.to_verify:
			self.show_success()
			self.manager.current = 'login'
		else:
			self.show_error_popup()

	def show_error_popup(self):
		popup = Popup(title='Error',
					  content=Label(text='Incorrect verification code!'),
					  size_hint=(0.8, 0.4))
		popup.open()

	def show_success(self):
		popup = Popup(title='Register successful',
					  content=Label(text='You successfuly register an account'),
					  size_hint=(0.8, 0.4))
		popup.open()
