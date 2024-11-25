from kivy.app import App
from kivy.uix.widget import Widget

class habitGame(Widget):
    pass

class habitApp(App):
    def build(self):
        return habitGame()
    
habitApp().run()