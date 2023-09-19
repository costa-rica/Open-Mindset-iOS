from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, ColorProperty, StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import platform
from kivy.core.window import Window
import os
from dotenv import load_dotenv
import json



if platform not in ['ios','android']:
  Window.size = (960, 1704)# iPhone 13 Mini
  print('Screen size set by application')

def hex_to_rgba(hexcolor, alpha=1.0):
    r = int(hexcolor[1:3], 16) / 255.0
    g = int(hexcolor[3:5], 16) / 255.0
    b = int(hexcolor[5:7], 16) / 255.0
    return (r, g, b, alpha)


class ScreenManagerMain(ScreenManager):
    pass
class HomeScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.hex_to_rgba = hex_to_rgba
        print("--- HomeScreen ---")
        print("db_path: ", MainApp().custum_config)
    
    def on_text_validate(self, widget):
        print("on_text_validate")
        print(widget.text)
        
        # Write the text to the .json file
        self.write_to_json(widget.text)
        
        self.parent.current = "screen_parent"
        
    def write_to_json(self, text):
        # Construct the full path for the .json file
        file_path = os.path.join(MainApp().custum_config.db_path, 'api_token.json')
        
        # Write the data to the .json file
        with open(file_path, 'w') as json_file:
            json.dump({"api_token": text}, json_file)




class ParentScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.hex_to_rgba = hex_to_rgba
    def go_to_home(self):
        self.parent.current = "screen_home" #ScreenManagerMain

class ChatScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class NavMenu(BoxLayout):

    def clicked_btn(self, widget):
        print(f"clicked: {widget.text}")
        print("NavMenu button clicked")
        print(self.parent)
        print(self.parent.parent)
        print("Parent Screen: ", self.parent.parent.parent)
        print("ScreenManager: ", self.parent.parent.parent.children[0].children[1])
        self.child_sm = self.parent.parent.parent.children[0].children[1]
        if widget.text == "Chat":
            self.child_sm.current = "screen_chat"
        if widget.text == "Settings":
            self.child_sm.current = "screen_settings"

class ConfigObject():
    def __init__(self):

        if platform == 'ios':
            print("--- Thinks its iOS ---")
            # Use Pyobjus to access iOS APIs to get the Documents directory
            from pyobjus import autoclass
            NSFileManager = autoclass('NSFileManager')
            paths = NSFileManager.defaultManager().URLsForDirectory_inDomains_(9, 1)  # 9 for Document directory
            self.db_path = paths.objectAtIndex_(0).path()
        else:
            print("--- NOT  iOS ---")
            # Load environment variables from the .env file
            load_dotenv()

            # Fetch the PROJECT_DB_DIR from the environment variables
            self.db_path = os.environ.get("PROJECT_DB_DIR")
            # print(f"-----> self.db_path:  {self.db_path}")
            # Check if the directory exists, and create it if not
            if self.db_path and not os.path.exists(self.db_path):
                try:
                    os.makedirs(self.db_path)
                except Exception as e:
                    # Handle the exception (e.g., log it, raise a custom error, etc.)
                    print(f"Error creating directory {self.db_path}: {e}")

class MainApp(MDApp):
    custum_config = None  # declare the attribute at the class level

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.custum_config = ConfigObject()
        print("--- set config ---")
        print(f"------> self.config.db_path: {self.custum_config.db_path}")
    def build(self):
        print("--- build ----")
        print("custum_config.db_path: ", self.custum_config.db_path)
        return Builder.load_file('OpenMindset.kv')

MainApp().run()