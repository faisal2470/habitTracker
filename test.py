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
from kivy.clock import Clock
import calendar as cal

class CustomBoxLayout(BoxLayout):
    pass

class CustomColorLabel(Label):
    pass

class CustomTabbedPanel(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(current_tab=self.update_tab_colors)
        self.bind(size=self.adjust_tab_width)
        self.do_default_tab = False
        # Schedule setting the default tab after the widget is built
        Clock.schedule_once(self.set_default_tab, 0)

    def update_tab_colors(self, *args):
        for header in self.tab_list:
            if isinstance(header, TabbedPanelHeader):
                if header.state == "down":
                    header.background_color = (0.7, 0.7, 0.7, 1) # Grey Colour
                else:
                    header.background_color = (0.9, 0.9, 0.9, 1)

    def adjust_tab_width(self, *args):
        num_tabs = len(self.tab_list)
        if num_tabs > 0:
            self.tab_width = self.width/num_tabs - 2

    def set_default_tab(self, *args):
        # Set the default tab to the Home tab
        for tab in self.tab_list:
            if tab.text == "Home":  # Match the tab by its text
                self.switch_to(tab)
                break


class Home(TabbedPanelItem):
    pass

class Habit(TabbedPanelItem):
    pass

class Todo(TabbedPanelItem):
    pass

class ProductivityApp(App):
    def build(self):
        return CustomBoxLayout()
    
ProductivityApp().run()