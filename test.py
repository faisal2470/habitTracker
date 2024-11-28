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

class CustomBoxLayout(BoxLayout):
    pass

class ProductivityApp(App):
    today = cal.datetime.datetime.now()
    current_week = int(today.strftime('%W'))
    week = current_week

ProductivityApp().run()