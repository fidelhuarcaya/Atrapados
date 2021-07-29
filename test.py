

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics.context_instructions import Color
from kivy.uix.label import Label
from kivy.lang.builder import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty

Builder.load_file('test.kv')
class ScreenManagement(ScreenManager):
    pass


class Screen1(Screen):
    name_x = StringProperty('')

    def update_info(self):
        self.name_x = self.ids.nombre.text
        print(self.name_x)


class Screen2(Screen):
    names = StringProperty('')

    def on_pre_enter(self, *args):
        self.names = "Hola : " + self.manager.ids.Screen1.name_x


class MainApp(App):
    def build(self):
        return ScreenManagement()


if __name__ == "__main__":
    MainApp().run()
