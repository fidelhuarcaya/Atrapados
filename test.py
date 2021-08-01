

from kivy.uix.button import Button
from kivy.lang import Builder
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

#Builder.load_file('test.kv')


class ScreenOne(Screen):
    pass


class ScreenTwo(Screen):
    text = StringProperty('')

    def on_pre_enter(self, *args):
        print("\nScreenTwo.on_pre_enter:")

        btn = Button(text="word is here", on_release=self.pressedFunction)
        self.ids.container.add_widget(btn)

        btn1 = Button(text="another word is here",
                      on_release=self.pressedFunction)
        self.ids.container.add_widget(btn1)

    def pressedFunction(self, instance, *args):
        self.text = str(instance.text)      # populate before switching screen
        self.manager.current = "three"  # switch screen


class ScreenThree(Screen):
    def on_pre_enter(self, *args):
        self.ids.my_label.text = self.manager.ids.screen_two.text


class ScreenManagement(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return Builder.load_file("test.kv")


if __name__ == "__main__":
    MainApp().run()
