from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem, TabbedPanelHeader
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle
import calendar as cal
from tab_enum import TabType

class CustomBoxLayout(BoxLayout):
    pass

class CustomColorLabel(Label):
    pass

class CustomTabbedPanel(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_tabs()
        self.bind(current_tab=self.update_tab_colors)
        self.do_default_tab = False

    def add_tabs(self):
        # Add Tabs
        self.add_widget(self.create_tab(TabType.HOME))
        self.add_widget(self.create_tab(TabType.HABIT))
        self.add_widget(self.create_tab(TabType.TODO))

    def create_tab(self, tab_type):
        # Dynamically create the tab from KV layout
        tab = TabbedPanelItem(text=tab_type.value)
        
        return tab

    def update_tab_colors(self, *args):
        for header in self.tab_list:
            if isinstance(header, TabbedPanelHeader):
                if header.state == "down":
                    header.background_color = (0.7, 0.7, 0.7, 1) # Grey Colour
                else:
                    header.background_color = (0.9, 0.9, 0.9, 1)

class ProductivityApp(App):
    def build(self):
        return CustomBoxLayout()
    
ProductivityApp().run()