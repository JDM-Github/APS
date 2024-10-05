from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

class SuccessScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
		
		self.label = Label(text="Verification Successful!", font_size=32)
		layout.add_widget(self.label)
		
		self.add_widget(layout)

	def display_design(self):
		pass