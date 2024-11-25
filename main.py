from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle

class CustomBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add a Canvas instruction for the background
        with self.canvas.before:
            Color(0.7, 0.7, 0.7, 1) # Light Blue Background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # Bind size and position updates to keep the background in place
        self.bind(size=self._rect_update, pos=self._rect_update)

    def _rect_update(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class CustomLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add a canvas to the background
        with self.canvas.before:
            Color(0.5, 0.5, 0.2, 1) # Olive Green Background
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)
        # Bind size and position updates to keep the background in place
        self.bind(size=self._rect_update, pos=self._rect_update)
        # self.color = (0.82, 0.71, 0.55, 1) # Beige Colour

    def _rect_update(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class HabitTrackerApp(App):
    def build(self):
        # Root Layout
        self.root_layout = CustomBoxLayout(orientation='vertical', padding=10, spacing=10)

        # Title Label
        title_label = CustomLabel(
            text="Habit Tracker",
            font_size='24sp',
            size_hint=(1, None),
            height=50,
            halign='center',
            valign='middle'
        )
        title_label.bind(size=title_label.setter('text_size'))  # Align text properly
        self.root_layout.add_widget(title_label)

        # Input box to add a new habit
        input_layout = BoxLayout(size_hint=(1, None), height=50, spacing=10)
        self.habit_input = TextInput(hint_text="Enter a new habit", multiline=False)
        add_button = Button(text="Add", size_hint=(None, 1), width=100)
        add_button.bind(on_press=self.add_habit)
        input_layout.add_widget(self.habit_input)
        input_layout.add_widget(add_button)
        self.root_layout.add_widget(input_layout)

        # Scrollable area for habits
        self.habit_scroll = ScrollView(size_hint=(1, 1))
        self.habit_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.habit_list.bind(minimum_height=self.habit_list.setter('height'))  # Adjust size for scrolling
        self.habit_scroll.add_widget(self.habit_list)
        self.root_layout.add_widget(self.habit_scroll)

        return self.root_layout
    
    def add_habit(self, instance):
        habit_text = self.habit_input.text.strip()
        if habit_text:
            # Create a new habit row
            habit_row = BoxLayout(size_hint_y=None, height=50, spacing=10)
            
            habit_label = Label(text=habit_text, size_hint=(0.8, 1))
            toggle_button = Button(text="Incomplete", size_hint=(0.2, 1))
            toggle_button.bind(on_press=self.toggle_habit)

            habit_row.add_widget(habit_label)
            habit_row.add_widget(toggle_button)
            
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
    
HabitTrackerApp().run()