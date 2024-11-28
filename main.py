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
import datetime as dt

class CustomBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add a Canvas instruction for the background
        with self.canvas.before:
            Color(0.7, 0.7, 0.7, 1) # Light Grey Background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # Bind size and position updates to keep the background in place
        self.bind(size=self._rect_update, pos=self._rect_update)

    def _rect_update(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class CustomColorLabel(Label):
    def __init__(self, bg_color, **kwargs):
        super().__init__(**kwargs)
        # Add a canvas to the background
        with self.canvas.before:
            Color(*bg_color) # Olive Green Background
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)
        # Bind size and position updates to keep the background in place
        self.bind(size=self._rect_update, pos=self._rect_update)
        # self.color = (0.82, 0.71, 0.55, 1) # Beige Colour

    def _rect_update(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class CustomTabbedPanel(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set a consistent background color for the tab content area
        self.background_color = (0.7, 0.7, 0.7, 1)  # Light Grey Background
        self.background_normal = ""  # Disable default background texture

        self.bind(current_tab=self.update_tab_colors)

    def update_tab_colors(self, *args):
        for header in self.tab_list:
            if isinstance(header, TabbedPanelHeader):
                if header.state == "down":
                    header.background_color = (0.7, 0.7, 0.7, 1) # Grey Colour
                else:
                    header.background_color = (0.9, 0.9, 0.9, 1)

class ProductivityApp(App):
    def build(self):
        # Root Layout
        root_layout = CustomBoxLayout(orientation="vertical", padding=10, spacing=10)

        # Title Label for the Main Screen
        title_label = CustomColorLabel(
            bg_color=(0.5, 0.5, 0.2, 1),  # Olive Green Background
            text="Productivity App",
            font_size='24sp',
            size_hint=(1, None),
            height=60,
            halign='center',
            valign='middle'
        )
        title_label.bind(size=title_label.setter('text_size'))  # Center the text
        root_layout.add_widget(title_label)

        # Tabbed Panel
        tab_panel = CustomTabbedPanel(
            tab_pos = 'bottom_left',
            tab_height = 50
        )

        # Adjust the tab width
        tab_panel.bind(size=self.adjust_tab_width)

        # Home Tab
        home_tab = self.create_home_tab()
        tab_panel.add_widget(home_tab)

        # Habit Tracker Tab
        habit_tab = self.create_habit_tracker_tab()
        tab_panel.add_widget(habit_tab)

        # To-Do List Tab
        todo_tab = self.create_todo_list_tab()
        tab_panel.add_widget(todo_tab)

        # Set Default Tab as False
        tab_panel.do_default_tab = False

        # Manually select the Home Tab as the default tab
        tab_panel.switch_to(home_tab)

        # Trigger an initial update of tab colors
        tab_panel.update_tab_colors()

        root_layout.add_widget(tab_panel)

        return root_layout

    
    def create_home_tab(self):

        home_tab = TabbedPanelItem(text="Home")
        home_tab.bind(size=home_tab.setter("text_size"))
        layout = CustomBoxLayout(orientation='vertical')
        scroll_view = ScrollView(size_hint=(1, 1))

        header_row = GridLayout(cols=8, size_hint_y=None, height=30)
        days = cal.day_abbr[:]
        column = ['Time'] + days
        
        for col in column:
            header_row.add_widget(
                Label( 
                    text=col, 
                    color=(0, 0, 0, 1),
                    bold=True,
                    size_hint_y=None, 
                    height=40,
                    halign='center',
                    valign='middle'
                )
            )
        layout.add_widget(header_row)

        self.time_row = GridLayout(cols=8, size_hint_y=None)
        for t in [dt.time(i).strftime('%H:%M') for i in range(24)]:
            time_label = Label(
                text=t,
                size_hint=(1, None),
                height=30,
                color = (0, 0, 0, 1)
            )
            self.time_row.add_widget(time_label)
            
            for _ in range(7):
                cell = Label(
                    text="",
                    size_hint=(1, None),
                    height=30,
                    color=(0, 0, 0, 1)
                )
                self.time_row.add_widget(cell)
        
        self.time_row.bind(minimum_height=self.time_row.setter("height"))
        scroll_view.add_widget(self.time_row)

        layout.add_widget(scroll_view)
        home_tab.add_widget(layout)
        return home_tab



    def adjust_tab_width(self, instance, value):
        num_tabs = len(instance.tab_list)
        if num_tabs > 0:
            instance.tab_width = instance.width/num_tabs - 2

    def create_habit_tracker_tab(self):

        habit_tab = TabbedPanelItem(text="Habit Tracker")
        habit_tab.bind(size=habit_tab.setter("text_size"))
        layout = CustomBoxLayout(orientation='vertical', padding=10, spacing=10)

        # # Title Label
        # title_label = CustomColorLabel(
        #     bg_color=(0.5, 0.5, 0.2, 1),
        #     text="Habit Tracker",
        #     font_size='24sp',
        #     size_hint=(1, None),
        #     height=50,
        #     halign='center',
        #     valign='middle'
        # )
        # title_label.bind(size=title_label.setter('text_size'))  # Align text properly
        # layout.add_widget(title_label)

        # Input box to add a new habit
        input_layout = BoxLayout(size_hint=(1, None), height=50, spacing=10)
        self.habit_input = TextInput(hint_text="Enter a new habit", multiline=False)
        add_button = Button(text="Add", size_hint=(None, 1), width=100)
        add_button.bind(on_press=self.add_habit)
        input_layout.add_widget(self.habit_input)
        input_layout.add_widget(add_button)
        layout.add_widget(input_layout)

        # Scrollable area for habits
        self.habit_scroll = ScrollView(size_hint=(1, 1))
        self.habit_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.habit_list.bind(minimum_height=self.habit_list.setter('height'))  # Adjust size for scrolling
        self.habit_scroll.add_widget(self.habit_list)
        layout.add_widget(self.habit_scroll)

        habit_tab.add_widget(layout)
        return habit_tab

    def create_todo_list_tab(self):

        todo_tab = TabbedPanelItem(text="To-Do List")
        todo_tab.bind(size=todo_tab.setter("text_size"))
        layout = CustomBoxLayout(orientation='vertical', padding=10, spacing=10)

        todo_tab.add_widget(layout)
        return todo_tab
    
    def add_habit(self, instance):
        habit_text = self.habit_input.text.strip()
        if habit_text:
            # Create a new habit row
            habit_row = BoxLayout(size_hint_y=None, height=50, spacing=10)
            
            habit_label = CustomColorLabel(
                bg_color=(1, 1, 1, 1), # White color
                text=habit_text,
                color=(0, 0, 0, 1),
                size_hint=(0.8, 1)
            )

            toggle_button = Button(
                text="Incomplete", 
                size_hint=(0.2, 1), 
                background_color = (1, 0, 0, 1), 
                background_normal = ""
            )
            toggle_button.bind(on_press=self.toggle_habit)
            
            delete_button = Button(
                text="Delete", 
                size_hint=(0.2, 1), 
                background_color = (0.3, 0.3, 0.3, 1), 
                background_normal = ""
            )
            delete_button.bind(on_press=self.delete_habit)

            habit_row.add_widget(habit_label)
            habit_row.add_widget(toggle_button)
            habit_row.add_widget(delete_button)
            
            self.habit_list.add_widget(habit_row)

            # Clear the input box
            self.habit_input.text = ""

    def toggle_habit(self, instance):
        # Toggle habit completion status
        if instance.text == "Incomplete":
            instance.text = "Complete"
            instance.background_color = (0, 1, 0, 1)  # Green
        else:
            instance.text = "Incomplete"
            instance.background_color = (1, 0, 0, 1)  # Red

    def delete_habit(self, instance):
        self.habit_list.remove_widget(instance.parent)
    
ProductivityApp().run()