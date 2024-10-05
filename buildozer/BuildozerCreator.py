import os
import sys
import json
from .all_mode import ALL_MODE
from kivy.config import Config
Config.set('graphics', 'width', 800)
Config.set('graphics', 'height', 700)
Config.write()

from kivy.core.window import Window
Window.size = (800, 700)
Window.left = 5
Window.top = 30

from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.utils import get_color_from_hex as GetColor


from kivy.app import App
from kivy.core.text import LabelBase
from kivy.core.audio import SoundLoader
soundClick = SoundLoader.load(r"assets/wav/click.wav")

LabelBase.register(
	name="consolas",
	fn_regular="assets/font/consolas/consolas_regular.ttf",
	fn_bold="assets/font/consolas/consolas_bold.ttf",
	fn_italic="assets/font/consolas/consolas_italic.ttf",
	fn_bolditalic="assets/font/consolas/consolas_italic_bold.ttf")

class Theme:
	MAIN_BG_SOURCE    = r"assets/JDMBG.png"

	WINDOW_BACKGROUND = "#000000"
	MAIN_BACKGROUND   = "#000000"
	THEME_FG          = "#FFFFFF"
	THEME_COLOR       = "#03d5f5"

	BLUE_FG           = "#03d5f5"
	ENTRY_BLUE_FG     = "#03d5f5"

	BUTTON_LINE       = "#03d5f5"
	BUTTON_FG         = "#FFFFFF"
	BUTTON_COLOR      = "#000000"
	BUTTON_PRESSED    = "#03d5f5"
	BUTTON_SELECTION  = "#03d5f555"

	EXIT_LINE           = "#03d5f5" 
	EXIT_COLOR          = "#000000"
	EXIT_FG             = "#FFFFFF"

	MENU_COLOR          = "#03d5f5"
	MENU_BUTTON_COLOR   = "#FFFFFF"
	MENU_BUTTON_PRESSED = "#000000"
	RESULT_LINE         = "#03d5f5"
	RESULT_BOX          = "#000000"




class CustomLabel(Label):
	
	def __init__(self, name: str, Color: str, size: list[int, int], pos: list[int, int], **kwargs):
		super().__init__(**kwargs)
		self.font_name = "consolas"
		self.font_size = "13sp"
		self.color     = GetColor(Color)
		self.size      = size
		self.pos       = pos  
		self.text      = name 
		self.markup    = True

class CustomWidget(Widget):

	def __init__(self, pos: list[int, int], size: list[int, int], name: str, autoCall: bool = True, **kwargs):
		super().__init__(**kwargs)
		self.labelMode   = False
		self.selector    = False
		self.toggleMode  = False
		self.activate    = False
		self.func_binder = lambda: None
		self.clicked     = False
		self.name        = name
		self.size        = size
		self.pos         = pos

		if autoCall:
			self.displayDesign(
			App.get_running_app().CT.BUTTON_LINE,
			App.get_running_app().CT.BUTTON_COLOR,
			App.get_running_app().CT.BUTTON_PRESSED,
			App.get_running_app().CT.BUTTON_FG)
			self.bind(pos=self.bindCanvas)
	
	def displayDesign(self,
		ColorLine: str, Color: str, ColorPressed: str, ColorForeground: str,
		Radius: list[int, int, int, int] = [10, 10, 10, 10], Source: str = ""):

		self.clear_widgets()
		self.canvas.clear()

		self.buttonLine    = ColorLine
		self.buttonColor   = Color
		self.buttonPressed = ColorPressed
		self.buttonFG      = ColorForeground
		self.mainLabel     = CustomLabel(self.name, self.buttonFG, self.size, self.pos, font_name = "consolas")

		self.setCanvas(self.buttonLine, self.buttonColor, Radius, Source)
		self.add_widget(self.mainLabel)

	def setCanvas(self, color1: str, color2: str, radius : list = [10, 10, 10, 10], Source: str = ""):
		with self.canvas:
			thickness = 1
			self.color1 = Color(rgba=GetColor(color1))
			self.rect1  = RoundedRectangle(
				radius=radius,
				size=(self.width+(thickness*2), self.height+(thickness*2)),
				pos=(self.x-thickness, self.y-thickness) )

			self.color2 = Color(rgba=GetColor(color2))
			self.rect2  = RoundedRectangle( source=Source, radius=radius, size=self.size, pos=self.pos )
	
	def cfunctions(self):
		if self.toggleMode:
			if self.activate:
				self.activate = False
				self.color2.rgb = GetColor(self.buttonColor)
				return
			self.activate = True
		self.color2.rgb = GetColor(self.buttonPressed)
	def functions(self): ...

	def bindCanvas(self, *_):
		self.mainLabel.pos = self.pos
		self.rect1.pos     = (self.x-1, self.y-1)
		self.rect2.pos     = self.pos
	
	def SizebindCanvas(self, *_):
		self.mainLabel.size = self.size
		self.rect1.size     = (self.width+2, self.height+2)
		self.rect2.size     = self.size

	def on_touch_down(self, touch):
		if self.labelMode: return super().on_touch_down(touch)
		if self.collide_point(*touch.pos):
			self.cfunctions()
			soundClick.play()
			self.clicked = True
		return super().on_touch_down(touch)

	def on_touch_up(self, touch):
		if self.labelMode: return super().on_touch_up(touch)
		if self.clicked:
			self.functions()
			self.func_binder()
			self.clicked = False
			if self.selector is False and self.toggleMode is False:
				if hasattr(self, "color2"): self.color2.rgb = GetColor(self.buttonColor)
		return super().on_touch_up(touch)

class CustomTextInput(TextInput):

	def __init__(self, text, **kwargs):
		super().__init__(**kwargs)
		col = App.get_running_app().CT
		self.foreground_color = GetColor(col.BLUE_FG)
		self.hint_text_color = GetColor(col.BLUE_FG)
		self.selection_color = GetColor(col.BUTTON_SELECTION)
		self.cursor_color = GetColor(col.ENTRY_BLUE_FG)
		self.background_color = GetColor(col.MAIN_BACKGROUND)
		self.background_normal = ""
		self.background_active = ""
		self.font_size = "12sp"
		self.text = text
		self.hint_text = "None"
		self.multiline = False
		self.write_tab = False
		self.font_name = "consolas"

class SetWidget(BoxLayout):
	
	def __init__(self, mode, index, par, **kwargs):
		super().__init__(**kwargs)
		self.size_hint_y = None
		self.height = Window.height*0.05
		self.spacing = dp(5)

		self.mode_Text = mode
		self.index = index
		self.orientation = "horizontal"

		self.con = par.config
		mode = par.allModesList
		if not self.con.get(self.mode_Text):
			par.config[self.mode_Text] = {
				"Text": mode[self.index][1],
				"Activate": mode[self.index][2]
			}

		self.displayActivator()
		self.displayMode()
		self.displayTextInput()
	
	def displayActivator(self):
		self.activator = CustomWidget((0, 0), (Window.width*0.8, Window.height*0.05), "X")
		self.activator.mainLabel.font_size = "16sp"
		self.activator.bind(size=self.activator.SizebindCanvas)
		self.activator.toggleMode = True

		if self.con.get(self.mode_Text).get("Activate"):
			self.activator.cfunctions()

		self.activator.size_hint = (0.1, None)
		self.add_widget(self.activator)
	
	def displayMode(self):
		self.mode = CustomWidget((0, 0), (Window.width*0.8, Window.height*0.05), self.mode_Text)
		self.mode.mainLabel.font_size = "10sp"
		self.mode.bind(size=self.mode.SizebindCanvas)
		self.mode.labelMode = True
		self.mode.size_hint = (0.4, None)
		self.add_widget(self.mode)

	def displayTextInput(self):
		self.txtinput = CustomTextInput(self.con.get(self.mode_Text).get("Text"), size=(Window.width*0.8, Window.height*0.05))
		self.txtinput.size_hint = (0.5, None)
		self.add_widget(self.txtinput)


class MainWidget(Widget):
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.size = Window.size
		with self.canvas:
			Color(rgb=GetColor(App.get_running_app().CT.MAIN_BACKGROUND))
			Rectangle(size=self.size)
			self.CmainBg = Color(rgba=GetColor("ffffff66"))
			self.mainBg = Rectangle(size=self.size, source=App.get_running_app().CT.MAIN_BG_SOURCE)
		self.configureJson()
		self.displayTitle("Buildozer Build")
		self.displaygrid()

	def displayTitle(self, text: str):
		self.title = Label(
			font_size= "32sp",
			font_name= "consolas",
			color    = GetColor(App.get_running_app().CT.MENU_BUTTON_COLOR),
			size     = (Window.width, Window.height*0.1),
			pos      = (0, Window.height*0.9),
			text     = text)

		with self.canvas:
			Color(rgb=GetColor(App.get_running_app().CT.MENU_COLOR))
			Rectangle(size=self.title.size, pos=self.title.pos)
		self.add_widget(self.title)

	def configureJson(self):
		self.config = dict()
		if not os.path.exists(os.path.abspath('jsons')): os.mkdir(os.path.abspath('jsons'))
		if not os.path.exists(os.path.abspath("jsons/build-config.json")):
			with open(os.path.abspath("jsons/build-config.json"), "w") as f: f.write("{}")
		with open(os.path.abspath("jsons/build-config.json")) as f:
			self.config = json.load(f)

	def displaygrid(self):
		self.grid   = GridLayout(size_hint_y=None, cols=1, padding="10dp", spacing="5dp")
		self.scroll = ScrollView(
			size=(Window.width*0.9, Window.height*0.76),
			pos=(Window.width*0.05, Window.height*0.12))

		self.grid.bind(minimum_height=self.grid.setter('height'))
		with self.canvas:
			Color(rgb=GetColor(App.get_running_app().CT.RESULT_BOX), a=0.8)
			RoundedRectangle(size=self.scroll.size, pos=self.scroll.pos, radius=[10, 10, 10, 10])
		
		self.submitButton = CustomWidget(
			size=((Window.width * 0.82, Window.height*0.05)),
			pos=(Window.width*0.09, ((Window.height - ((Window.height*0.2)*3)) - (Window.height*0.01) - ((((Window.height*0.2) / 4) * 1.5) * (4+1)) )),
			name="Build Buildozer", autoCall=True
		)
		self.submitButton.func_binder = lambda *_ : self.buildBuildozer()
		self.add_widget(self.submitButton)
		self.scroll.add_widget(self.grid)
		self.add_widget(self.scroll)
		
		self.allModes()
		self.displayAllModes()
	
	def saveConfig(self):
		for mode in self.allSetModes:
			self.config[mode.mode_Text] = {
				"Text" : mode.txtinput.text,
				"Activate": mode.activator.activate,
			}
		if not os.path.exists(os.path.abspath("jsons")): os.mkdir(os.path.abspath("jsons"))
		with open(os.path.abspath("jsons/build-config.json"), "w") as f:
			json.dump(self.config, f, indent=4, separators=(',', ': '))

	def buildBuildozer(self):
		self.saveConfig()
		dynamic_content = "\n".join(
			[f"{self.setComment(self.allModesList[i][3])}{'' if self.config.get(key).get('Activate') else '# '}{key} = {self.config.get(key).get('Text')}{self.allModesList[i][4]}"
			 for i, key in enumerate(self.config)]
		)
	
		with open(os.getcwd() + "/buildozer/buildozer_template.spec", "r") as template_file:
			template_content = template_file.read()
	
		formatted_content = template_content.format(dynamic_content=dynamic_content)    
		with open(os.getcwd() + "/buildozer.spec", "w", encoding="utf-8") as f:
			f.write(formatted_content)
		self.buildYml()

	def buildYml(self):

		if not os.path.exists(os.path.abspath(".github")):
			os.mkdir(os.path.abspath(".github"))
		if not os.path.exists(os.path.abspath(".github/workflows")):
			os.mkdir(os.path.abspath(".github/workflows"))

		with open('buildozer/yml_template.txt', 'r') as file:
			template = file.read()

		string = template.format(
			package_name=self.config.get('package.name').get('Text'),
			artifact_name=f"{self.config.get('package.name').get('Text')}-{self.config.get('version').get('Text')}"
		)
		build_name = f"build-{os.path.splitext(self.config.get('package.domain').get('Text'))[1][1:]}"
		with open(os.path.abspath(f".github/workflows/{build_name}.yml"), "w") as f:
			f.truncate(0)
			f.write(string)

	def setComment(self, text):
		if not text: return text
		newText = str()
		for t in text:
			if t == '\n': newText += t + '# '
			else: newText += t
		return '# ' + newText + '\n'

	def allModes(self):
		self.allModesList = ALL_MODE

	def displayAllModes(self):
		self.allSetModes : list[SetWidget] = list()
		for i, mode in enumerate(self.allModesList):
			self.allSetModes.append(SetWidget(mode[0], i, self))
			self.grid.add_widget(self.allSetModes[i])


class BuildozerCreator(App):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.CT = Theme()

	def build(self):
		self.mainWid = MainWidget()
		return self.mainWid

