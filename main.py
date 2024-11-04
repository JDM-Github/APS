from functools import partial
from kivy.config import Config
WIDTH  = int(750  * 0.8) 
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
import re
import json
import datetime
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.clock import Clock
from handle_request import LoadingPopup, RequestHandler

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
Builder.load_file('screens/employee_menu.kv')
Builder.load_file('screens/employee_shift.kv')
Builder.load_file('screens/employee_attendance.kv')
Builder.load_file('screens/employee_attendance_report.kv')
Builder.load_file('screens/employee_profile.kv')

Builder.load_file('screens/popup/yes_no.kv')
Builder.load_file('screens/popup/alert_popup.kv')
Builder.load_file('screens/popup/add_employee.kv')
Builder.load_file('screens/popup/attendance_popup.kv')
Builder.load_file('screens/popup/project_popup.kv')
Builder.load_file('screens/popup/detail_report.kv')
Builder.load_file('screens/popup/employee_details.kv')

Builder.load_file('screens/admin/admin_dashboard.kv')
Builder.load_file('screens/admin/admin_attendance.kv')
Builder.load_file('screens/admin/admin_schedule.kv')
Builder.load_file('screens/admin/admin_employee.kv')
Builder.load_file('screens/admin/admin_project.kv')
Builder.load_file('screens/admin/admin_project_view.kv')

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.uix.pickers import MDTimePickerDialVertical
from kivymd.uix.pickers import MDModalDatePicker
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import DictProperty, ListProperty

from kivy.metrics import dp, sp

class LabelLabel(BoxLayout):
    text = StringProperty("")
    text2 = StringProperty("")
    label1_size_hint = ListProperty([0, 0])

class TextInputImage(Widget):
    text = StringProperty("")
class EvenLabel(Label): pass
class OddLabel (Label): pass
class TableButton(Button): pass
class CustomButton(Button):
    default_color = ListProperty([])
    pressed_color = ListProperty([])

class CustomToggleButton(ToggleButton): pass

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

class CustomPopup    (Popup): pass
class Profile        (Screen): pass
class ApplyNow       (Screen): pass
class Job            (Screen): pass
class DashboardScreen(Screen): pass

class Login          (Screen):

    email = StringProperty("")
    password = StringProperty("")

    def login_account(self):
        if self.email == "admin":
            self.manager.go_to_admin_dashboard()
            return

        RequestHandler.request_loader(
        lambda: RequestHandler.create_req_suc_error("post", "users/login", {
            'email': self.email,
            'password': self.password,
        }, self.on_sucess, self.on_error))

    def on_sucess(self, response):
        popup = AlertPopup(label_text="Successfully login employee account")
        popup.open()

        app = App.get_running_app()
        app.main_state = response['user']
        app.save_json_config('main_state.json', app.main_state)
        self.manager.go_to_employee_dash()

    def on_error(self, error):
        popup = AlertPopup(label_text="Error logging employee account: " + str(error['message']))
        popup.open()

class Register       (Screen): pass
class JobInterview   (Screen): pass
class TableView      (ScrollView): pass


class CustomDropDown   (DropDown   ): pass
class AdminTable       (StackLayout): pass
class AttendancePopup  (Popup      ): pass
class ProjectPopup     (Popup      ):
    project_name = StringProperty("")
    project_location = StringProperty("")
    project_type = StringProperty("Emergency Repair")
    start_date = StringProperty("")
    end_date = StringProperty("")
    project_description = StringProperty("")
    project_managers = DictProperty()

    def __init__(self, values, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        name_id_dict = {f"{person['firstName']} {person['middleName']} {person['lastName']}": person['id'] for person in values}
        self.project_managers = name_id_dict

        self.ids.project_manager.values = self.project_managers.keys()

    def create_project(self):
        RequestHandler.request_loader(
        lambda: RequestHandler.create_req_suc_error("post", "projects/create-project", {
            'projectManager': self.project_managers[self.ids.project_manager.text],
            'projectName': self.project_name,
			'projectLocation': self.project_location,
			'projectType': self.project_type,
			'projectDescription': self.project_description,
			'startDate': self.start_date,
			'endDate': self.end_date,
        }, self.on_sucess, self.on_error))
    
    def on_sucess(self, response):
        self.dismiss()

        popup = AlertPopup(label_text="Successfully created project account")
        popup.bind(on_dismiss=lambda *_: self.manager.get_screen(self.manager.current).load_all_project())
        popup.open()

    def on_error(self, error):
        self.dismiss()
        popup = AlertPopup(label_text=error.get('nessage', "Error creating project"))
        popup.open()

class DetailReportPopup(Popup      ):
    project = DictProperty({
        'id': '',
        'projectManager': '',
        'projectName': '',
        'projectLocation': '',
        'projectType': '',
        'projectDescription': '',
        'startDate': '',
        'endDate': '',
        'projectEmployees': [],
        'createdAt': '',
        'updatedAt': '',
        'Users': {'firstName': '', 'middleName': '', 'lastName': ''}})

class AddEmployee      (Popup      ):

    first_name = StringProperty("")
    middle_initial = StringProperty("")
    last_name = StringProperty("")
    gender_selected = StringProperty("Male")
    email = StringProperty("")
    password = StringProperty("")
    department = StringProperty("")
    skills = ["Leadership", "Communication", "Teamwork", "Problem Solving", "Time Management", "Adaptability", "Creativity", "Work Ethic", "Critical Thinking", "Flexibility"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.populate_skills()

    def populate_skills(self):
        for skill in self.skills:
            skill_button = CustomToggleButton(
                text=skill,
                size_hint_y=None,
                height=Window.height * 0.04
            )
            self.ids.all_skills.add_widget(skill_button)

    def get_skills(self):
        all_skills = []
        widget = self.ids.all_skills

        for child in widget.children:
            if child.state == "down":
                all_skills.append(child.text)
        return all_skills

    def create_account(self):
        RequestHandler.request_loader(
        lambda: RequestHandler.create_req_suc_error("post", "users/create-user", {
            'firstName': self.first_name,
            'lastName': self.last_name,
            'middleName': self.middle_initial,
            'gender': self.gender_selected,
            'email': self.email,
            'password': self.password,
            'department': self.department,
            'skills': self.get_skills(),
            'isManager': self.ids.is_manager.state == "down"
        }, self.on_sucess, self.on_error))
    
    def on_sucess(self, response):
        self.dismiss()
        popup = AlertPopup(label_text="Successfully created employee account")
        popup.open()

    def on_error(self, error):
        self.dismiss()
        popup = AlertPopup(label_text="Error creating employee account: " + str(error['nessage']))
        popup.open()

class EmployeeDetail   (Popup      ):
    full_name = StringProperty()
    gender = StringProperty()
    location = StringProperty()
    email = StringProperty()
    department = StringProperty()
    position = StringProperty()
    start_date = StringProperty()
    is_manager = StringProperty()

    def load_all_skills(self, employee):
        widget = self.ids.all_skills
        widget.clear_widgets()

        skills = employee['skills']
        for skill in skills:
            widget.add_widget(
                LabelLabel(
                    size_hint_y=None, height=Window.height * 0.05,
                    text=skill, label1_size_hint=[1, 1]))

class AlertPopup       (Popup      ):
    label_text = StringProperty("")
class YesorNoPopup     (Popup      ):
    label_text = StringProperty("")

    def on_yes(self):
        self.result = True
        self.dismiss()

    def on_no(self):
        self.result = False 
        self.dismiss() 

# EMPLOYEE SCREENS
class EmployeeDashboard (Screen): pass
class EmployeeMenu      (Screen): pass
class EmployeeAttendance(Screen): pass
class EmployeeReport    (Screen): pass
class EmployeeSchedule  (Screen): pass
class EmployeeProfile   (Screen): pass


class AdminDashboard  (Screen):

    def load_all_employee(self):
        RequestHandler.request_loader(
        lambda: RequestHandler.create_req_suc_error("post", "users/get-all-employees", {}, self.on_success, self.on_error))

    def on_success(self, response):
        widget = self.ids.employee_table
        widget.clear_widgets()

        for index, user in enumerate(response['users']):
            if index % 2 == 0:
                label = EvenLabel(text=f"{user['lastName']}, {user['firstName']}", font_size=sp(12))
            else:
                label = OddLabel(text=f"{user['lastName']}, {user['firstName']}", font_size=sp(12))

            button = TableButton(text="VIEW")
            button.bind(on_release=partial(self.manager.view_employee, user))

            deact_button = CustomButton(text="DEACTIVATE" if not user['is_deactivated'] else "ACTIVATE")
            if not user['is_deactivated']:
                deact_button.default_color = 0.8, 0.2, 0.3, 1
                deact_button.pressed_color = 0.6, 0.1, 0.2, 1

            deact_button.bind(on_release=partial(self.deact_or_act_user, user))
            widget.add_widget(label)
            widget.add_widget(button)
            widget.add_widget(deact_button)

    def on_error(self, error):
        popup = AlertPopup(label_text=error.get('message', 'Error fetching projects'))
        popup.open()

    def add_employee(self):
        popup = AddEmployee()
        popup.open()

    def deact_or_act_user(self, user, *_):
        popup = YesorNoPopup()

        popup.label_text = f"Are you sure you want to {"deactivate" if not user['is_deactivated'] else "activate"} this account?"
        popup.bind(on_dismiss=lambda instance: self.deactivate_employee(instance, f"{user['firstName']} {user['firstName']}"))
        popup.open()

    def deactivate_employee(self, instance, name):
        if instance.result:
            print(f"User {name} clicked Yes!")


class AdminAttendance (Screen):

    def open_attendance(self):
        popup = AttendancePopup()
        popup.open()
    
    

class AdminSchedule          (Screen): pass
class AdminEmployeeAttendance(Screen): pass
class AdminProject           (Screen):

    def add_project(self):
        RequestHandler.request_loader(
        lambda: RequestHandler.create_req_suc_error("post", "users/get-all-manager", {}, self.on_user_sucess, self.on_user_error))

    def on_user_sucess(self, response):
        popup = ProjectPopup(response.get('managers', {}), self.manager)
        popup.open()

    def on_user_error(self, error):
        popup = AlertPopup(label_text=error.get('message', 'Cannot load add project'))
        popup.open()

    def load_all_project(self):
        RequestHandler.request_loader(
        lambda: RequestHandler.create_req_suc_error("post", "projects/get-all-projects", {}, self.on_sucess, self.on_error))

    def on_sucess(self, response):
        widget = self.ids.employee_table
        widget.clear_widgets()

        for index, project in enumerate(response['projects']):
            if index % 2 == 0:
                label = EvenLabel(text=project['projectName'], font_size=sp(10))
            else:
                label = OddLabel(text=project['projectName'], font_size=sp(10))
            
            button = TableButton(text="VIEW")
            button.bind(on_release=partial(self.manager.go_to_admin_project_view, project))

            widget.add_widget(label)
            widget.add_widget(button)

    def on_error(self, error):
        popup = AlertPopup(label_text=error.get('message', 'Error fetching projects'))
        popup.open()

class AdminProjectView       (Screen):

    project = DictProperty({
        'id': '',
        'projectManager': '',
        'projectName': '',
        'projectLocation': '',
        'projectType': '',
        'projectDescription': '',
        'startDate': '',
        'endDate': '',
        'projectEmployees': [],
        'createdAt': '',
        'updatedAt': '',
        'Users': {'firstName': '', 'middleName': '', 'lastName': ''}})

    def load_project(self, data):
        self.project = data

    def project_detail(self):
        popup = DetailReportPopup(project=self.project)
        popup.open()

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

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.transition = FadeTransition(duration=0.1)

    def go_to_login        (self):
        self.current = "login"

        app = App.get_running_app()
        app.main_state['id'] = ''
        app.save_json_config('main_state.json', app.main_state)

    def go_to_register     (self): self.current = "register"
    def go_to_dashboard    (self): self.current = "dashboard"
    def go_to_menu         (self): self.current = "menu"
    def go_to_job          (self): self.current = "job"
    def go_to_applynow     (self): self.current = "applynow"    
    def go_to_user_profile (self): self.current = "profile-user"
    def go_to_job_interview(self): self.current = "job-interview"

    def go_to_employee_menu      (self): self.current = "employee-menu"
    def go_to_employee_dash      (self): self.current = "employee-dashboard"
    def go_to_employee_attendance(self): self.current = "employee-attendance"
    def go_to_employee_schedule  (self): self.current = "employee-schedule"
    def go_to_employee_profile   (self): self.current = "employee-profile"
    def go_to_employee_report    (self): self.current = "employee-attendance-report"

    def go_to_admin_dashboard    (self):
        self.current = "admin-dashboard"
        self.get_screen(self.current).load_all_employee()

    def go_to_admin_attendance   (self): self.current = "admin-attendance"
    def go_to_admin_schedule     (self): self.current = "admin-schedule"
    def go_to_admin_eattendance  (self): self.current = "admin-employee-attendance"
    def go_to_admin_project      (self):
        self.current = "admin-project" 
        self.get_screen(self.current).load_all_project()

    def go_to_admin_project_view (self, data, _):
        self.current = "admin-project-view"
        self.get_screen(self.current).load_project(data)
    


    # FUNCTION
    def view_employee(self, employee, *_):
        full_name = f"{employee['firstName']} {employee['middleName']} {employee['lastName']}"
        gender = employee['gender']
        location = employee['location']
        email = employee['email']
        department = employee['department']
        position = employee['position']
        start_date = employee['startDate']
        is_manager = "YES" if employee['isManager'] else "NO"
    
        popup = EmployeeDetail(full_name=full_name, gender=gender,
            location=location, email=email, department=department, position=position,
            is_manager=is_manager, start_date=start_date)
        popup.load_all_skills(employee)
        popup.open()


class APSApp(MDApp):
    main_state = DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_state = self.load_json_config('main_state.json')

    def build(self):
        self.sm = Manager(self)

        if self.main_state.get('id'):
            self.sm.current = "employee-dashboard"
        return self.sm

    def load_json_config(self, filepath):
        with open(filepath, 'r') as file:
            content = file.read()

        # USED TO ALLOW COMMENT IN JSON
        content = re.sub(r'//.*', '', content)
        content = re.sub(r'/\*[\s\S]*?\*/', '', content)
        return json.loads(content)

    # SAVE JSON
    def save_json_config(self, filepath, data):
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)

    def apply_for_job(self):
        self.sm.go_to_job()
    
    def show_date_picker(self, widget, focus, min_is_date=False):
        if not focus:
            return
    
        def on_date_selected(*args):
            selected_date = date_dialog.get_date()[0]
            formatted_date = selected_date.strftime("%Y-%m-%d")
            widget.text = formatted_date
            date_dialog.dismiss()

        if min_is_date:
            date_dialog = MDModalDatePicker(
                min_date = datetime.date.today(),
                max_date = datetime.date.today() + datetime.timedelta(days=365)
            )
        else:
            date_dialog = MDModalDatePicker()
        date_dialog.pos = [
            widget.center_x - date_dialog.width / 2,
            widget.y - (date_dialog.height + dp(32)),
        ]
        date_dialog.bind(on_cancel=lambda *_: date_dialog.dismiss())
        date_dialog.bind(on_ok=on_date_selected)
        date_dialog.open()
    
    def show_time_picker(self, widget, focus):
        if not focus:
            return

        def on_date_selected(*args):
            selected_date = time_dialog.time
            widget.text = str(selected_date)
            time_dialog.dismiss()

        time_dialog = MDTimePickerDialVertical(
            
        )
        time_dialog.pos = [
            widget.center_x - time_dialog.width / 2,
            widget.y - (time_dialog.height + dp(32)),
        ]
        time_dialog.bind(on_cancel=lambda *_: time_dialog.dismiss())
        time_dialog.bind(on_ok=on_date_selected)
        time_dialog.open()

if __name__ == '__main__':
    APSApp().run()




