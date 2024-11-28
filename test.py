from kivy.app import App
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem, TabbedPanelHeader
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle
import calendar as cal

class ProductivityApp(App):
    def build(self):
        
        return RootLayout()
    
class RootLayout(BoxLayout):
    pass

ProductivityApp().run()