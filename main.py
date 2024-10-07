from kivy.config import Config
WIDTH  = int(750  * 0.5) 
HEIGHT = int(1400 * 0.5)

Config.set('graphics', 'width', WIDTH)
Config.set('graphics', 'height', HEIGHT)
Config.set('graphics', 'resizable', 0)
Config.write()

from kivy.utils import platform
from kivy.core.window import Window

if platform == "win":
	Window.size  = (WIDTH, HEIGHT)
	Window.top   = 30
	Window.left  = 1

import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder

Builder.load_file('widgets.kv')
Builder.load_file('screens/login.kv')
Builder.load_file('screens/register.kv')
Builder.load_file('screens/dashboard.kv')
Builder.load_file('screens/menu.kv')
Builder.load_file('screens/job.kv')
Builder.load_file('screens/applynow.kv')
Builder.load_file('screens/profile.kv')
Builder.load_file('screens/job_interview.kv')
Builder.load_file('screens/employee_dashboard.kv')
Builder.load_file('screens/employee_shift.kv')


from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty

class ResumeWidget(BoxLayout):
	selected_file = StringProperty("")
	
	def open_file_manager(self):
		file_manager_popup = FileManagerPopup(custom_radio=self)
		file_manager_popup.open()

	def set_selected_file(self, filename):
		self.selected_file = os.path.basename(filename)

class FileManagerPopup(Popup):
    custom_radio = ObjectProperty(None) 

    def __init__(self, custom_radio, **kwargs):
        super(FileManagerPopup, self).__init__(**kwargs)
        self.custom_radio = custom_radio

    def select_file(self, selection):
        if selection:
            selected_file = selection[0].split('/')[-1]
            self.custom_radio.set_selected_file(selected_file)
            self.dismiss()

class CustomPopup(Popup): pass
class Profile(Screen): pass
class ApplyNow(Screen): pass
class Job(Screen): pass
class DashboardScreen(Screen): pass
class Login(Screen): pass
class Register(Screen): pass
class JobInterview(Screen): pass

# EMPLOYEE SCREENS
class EmployeeDashboard(Screen): pass
class EmployeeSchedule(Screen): pass


class Menu(Screen):

	def open_terms(self):
		popup = CustomPopup(title="APS Terms")
		popup.text_content = "This is APS Terms"
		popup.open()

	def open_policy(self):
		popup = CustomPopup(title="APS Policy")
		popup.text_content = "This is APS Policy"
		popup.open()

class Manager(ScreenManager):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.transition = FadeTransition(duration=0.1)

	def go_to_login        (self): self.current = "login"
	def go_to_register     (self): self.current = "register"
	def go_to_dashboard    (self): self.current = "dashboard"
	def go_to_menu         (self): self.current = "menu"
	def go_to_job          (self): self.current = "job"
	def go_to_applynow     (self): self.current = "applynow"	
	def go_to_user_profile (self): self.current = "profile-user"
	def go_to_job_interview(self): self.current = "job-interview"

	def go_to_employee_dash    (self): self.current = "employee-dashboard"
	def go_to_employee_schedule(self): self.current = "employee-schedule"


class APSApp(App):
	def build(self):
		self.sm = Manager()
		return self.sm

	def apply_for_job(self):
		self.sm.go_to_job()

if __name__ == '__main__':
	APSApp().run()




