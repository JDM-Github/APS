from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.clock import Clock

from kivy.utils import get_color_from_hex as GetColor, get_random_color
from kivy.graphics import Rectangle, RoundedRectangle, Color, Line, Ellipse, Rotate, PushMatrix, PopMatrix


class LoadingPopup(Widget):
    def __init__(self, root, **kwargs):
        super().__init__(**kwargs)
        self.size = root.size
        
        with self.canvas:
            Color(0, 0, 0, 0.8)
            Rectangle(size=root.size)

            PushMatrix()
            self.rotation = Rotate(angle=50, origin=(self.width/2-5,self.height/2+30))
            Color(rgba=get_random_color())
            Ellipse(pos=(self.width/2 - 10, self.height/2+10), size=(20, 20))
            Color(rgba=get_random_color())
            Ellipse(pos=(self.width/2 + 10, self.height/2-10), size=(20, 20))
            PopMatrix()

            PushMatrix()
            self.rotation2 = Rotate(angle=50, origin=(self.width/2-5,self.height/2+30))
            Color(rgba=get_random_color())
            Ellipse(pos=(self.width/2 - 10, self.height/2-10), size=(20, 20))
            Color(rgba=get_random_color())
            Ellipse(pos=(self.width/2 + 10, self.height/2+10), size=(20, 20))
            PopMatrix()
        
        self.rotation_angle = 0
        Clock.schedule_interval(self.update_rotation, 1 / 30.0)
    
    def update_rotation(self, dt):
        self.rotation_angle = (self.rotation_angle + 10) % 360
        self.rotation.angle = self.rotation_angle
        self.rotation2.angle = 360 - self.rotation_angle
