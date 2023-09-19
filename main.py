from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, ColorProperty, StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout

class HomeScreen(Screen):
    # text_input_str = StringProperty("foo")
    def go_to_chat(self):
        print("Go to chat")
    
    def on_text_validate(self, widget):
        print("on_text_validate")
        print(widget.text)
        self.parent.current = "screen_chat"

class ParentScreen(Screen):
    pass

class ChatScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass


class MainApp(MDApp):
    def build(self):
        return Builder.load_file('OpenMindset.kv')

MainApp().run()