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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.today = cal.datetime.datetime.now()
        self.current_week = int(self.today.strftime('%W'))
        self.current_year = int(self.today.strftime('%Y'))
        Clock.schedule_once(self.get_ids, 0)
        Clock.schedule_once(self.create_header, 0)
        Clock.schedule_once(self.set_current_week, 0)
    
    def set_current_week(self, *args):
        self.week = self.current_week
        self.year = self.current_year
        self.week_num.text = f'{self.year}, Week {self.week}'
        dates = self.get_dates(self.week, self.year)
        self.week_dates = [self.ids[i] for i in self.ids.keys() if i.endswith('date')]
        for ind, date in enumerate(dates):
            self.week_dates[ind].text = date

    def change_week(self, dir='+', *args):
        if dir == '+':
            self.week += 1
            if self.week > 52:
                self.year += 1
                self.week = 1
        else:
            self.week -= 1
            if self.week == 0:
                self.year -= 1
                self.week = 52
        self.week_num.text = f'{self.year}, Week {self.week}'
        dates = self.get_dates(self.week, self.year)
        self.week_dates = [self.ids[i] for i in self.ids.keys() if i.endswith('date')]
        for ind, date in enumerate(dates):
            self.week_dates[ind].text = date

    def get_dates(self, week, year=2024, *args):
        start_of_week = cal.datetime.datetime.fromisocalendar(year, week, 1)
        dates = [(start_of_week + cal.datetime.timedelta(i)).strftime('%d/%m/%Y') for i in range(7)]

        return dates

    def create_header(self, *args):
        days = cal.day_abbr[:]
        for day in days:
            day_label = CustomColorLabel(
                bg_color=(0.4, 0.4, 0.4, 1),
                text=day, 
                color=(0, 0, 0, 1),
                bold=True,
                size_hint_y=None, 
                height=25,
                halign='center',
                valign='middle'
            )
            day_label.bind(size=day_label.setter("text_size"))
            self.header_row.add_widget(day_label)

    def get_ids(self, *args):
        self.root_layout = self.ids['root_layout']
        self.header_row = self.ids['header_row']
        self.week_row = self.ids['week_row']
        self.week_num = self.ids['week_num']
        self.time_column = self.ids['time_column']


class Habit(TabbedPanelItem):
    pass

class Todo(TabbedPanelItem):
    pass

class ProductivityApp(App):
    def build(self):
        self.root_layout = CustomBoxLayout()
        self.get_ids()

        return self.root_layout
    
    def get_ids(self):
        self.home_tab = self.root_layout.ids['home_tab']
        self.habit_tab = self.root_layout.ids['habit_tab']
        self.todo_tab = self.root_layout.ids['todo_tab']

ProductivityApp().run()