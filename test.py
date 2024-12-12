from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem, TabbedPanelHeader
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
import calendar as cal
from pandas import MultiIndex, DataFrame
from kivy.graphics import Color, Line, RoundedRectangle
from db_manager import DatabaseManager

##########################################################################
###############                                            ###############
##########                    USER INTERFACE                    ##########
###############                                            ###############
##########################################################################
class CustomBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(CustomBoxLayout, self).__init__(**kwargs)

class CustomColorLabel(Label):
    def __init__(self, **kwargs):
        super(CustomColorLabel, self).__init__(**kwargs)

class CustomTabbedPanel(TabbedPanel):
    def __init__(self, **kwargs):
        super(CustomTabbedPanel, self).__init__(**kwargs)
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

############################################################
####                                                    ####
##                        HOME TAB                        ##
####                                                    ####
############################################################

class Home(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)
        self.today = cal.datetime.datetime.now()
        self.current_week = int(self.today.strftime('%W'))
        self.current_year = int(self.today.strftime('%Y'))
        Clock.schedule_once(self.get_ids, 0)
        Clock.schedule_once(self.create_header, 0)
        Clock.schedule_once(self.set_current_week, 0)
        Clock.schedule_once(self.create_time_column, 0)

    def create_time_column(self, *args):
        for t in [cal.datetime.time(i).strftime('%H:%M') for i in range(24)]:
            time_label = CustomColorLabel(
                bg_color=(0.5, 0.5, 0.5, 1),
                text=t,
                size_hint=(1, None),
                height=40,
                color = (0, 0, 0, 1),
                halign='center',
                valign='middle'
            )
            time_label.bind(size=time_label.setter("text_size"))
            self.time_column.add_widget(time_label)

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
        col_list = []
        for day in days:
            col_list.append((day, 'name'))
            col_list.append((day, 'id'))
            col_list.append((day, 'start'))
            col_list.append((day, 'end'))
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
        cols = MultiIndex.from_tuples(col_list)
        self.week_schedule = DataFrame(columns=cols)

    def get_ids(self, *args):
        self.root_layout = self.ids['root_layout']
        self.header_row = self.ids['header_row']
        self.week_row = self.ids['week_row']
        self.week_num = self.ids['week_num']
        self.time_column = self.ids['time_column']

###########################################################
####                                                   ####
##                       HABIT TAB                       ##
####                                                   ####
###########################################################

class Habit(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(Habit, self).__init__(**kwargs)
        self.db_manager = DatabaseManager()

###########################################################
####                                                   ####
##                       TO-DO TAB                       ##
####                                                   ####
###########################################################

class Todo(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(Todo, self).__init__(**kwargs)
        self.db_manager = DatabaseManager()

    def open_todo_popup(self, todo_type, *args):
        if todo_type == 'Task':
            tid = 'TA.'
        if todo_type == 'Appointment':
            tid = 'AP.'
        if todo_type == 'Event':
            tid = 'EV.'
        popup = AddToDo(
            on_submit = self.get_todo,
            task_id = tid,
            title = f'Add {todo_type}'
        )
        popup.open()

    def get_todo(self, task, *args):
        print(task)

#########################################
#            ADD TO-DO POPUP            #
#########################################
class AddToDo(Popup):
    def __init__(self, on_submit, task_id, **kwargs):
        super(AddToDo, self).__init__(**kwargs)
        self.on_submit = on_submit
        self.task_id = task_id
        self.priorities = ['N', 'L', 'M', 'H', 'N']
        self.bgs = {'N':(0.17, 0.17, 0.17, 1), 'L':(0, 0, 1, 0.2), 'M':(0, 1, 0, 0.2), 'H':(0.5, 0, 0, 1)}
        Clock.schedule_once(self.get_ids, 0)

    def get_ids(self, *args):
        self.todo_title = self.ids['todo_title']
        self.start_date = self.ids['start_date']
        self.start_time = self.ids['start_time']
        self.end_time = self.ids['end_time']
        self.end_date = self.ids['end_date']
        self.priority = self.ids['priority_label']
        self.title_error = self.ids['title_error']
        self.sd_error = self.ids['sd_error']
        self.st_error = self.ids['st_error']
        self.ed_error = self.ids['ed_error']
        self.et_error = self.ids['et_error']
        self.priority_button = self.ids['priority_button']
        self.start_label = self.ids['start_label']
        self.description = self.ids['description']
        if self.task_id.startswith('AP'):
            self.priority.text = 'H'
            self.start_label.text += '[color=ff0000]*[/color]'
            with self.priority_button.canvas.before:
                    Color(*self.bgs[self.priority.text])
                    RoundedRectangle(size=self.priority_button.size, pos=self.priority_button.pos, radius=[5, 5, 5, 5])

    def toggle_priority(self, instance):
        if self.task_id.startswith('AP'):
            return
        for ind, val in enumerate(self.priorities):
            if self.priority.text == val:
                self.priority.text = self.priorities[ind + 1]
                with instance.canvas.before:
                    Color(*self.bgs[self.priority.text])
                    RoundedRectangle(size=instance.size, pos=instance.pos, radius=[5, 5, 5, 5])
                return

    def reset_border_color(self, instance, colour, error):
        if error == 'ti':
            self.title_error.text = ''
        if error == 'sd':
            self.sd_error.text = ''
        elif error == 'st':
            self.st_error.text = ''
        elif error == 'ed':
            self.ed_error.text = ''
        elif error == 'et':
            self.et_error.text = ''

        with instance.canvas.after:
            instance.canvas.after.clear()
            Color(*colour)
            Line(width=1, rectangle=(instance.x, instance.y, instance.width, instance.height))

    def submit_todo(self, *args):
        task = {}
        task['id'] = self.task_id
        err = 0
        f = 1
        if self.validate_task(self.todo_title.text, 'title'):
            task['title'] = self.todo_title.text
        else:
            self.reset_border_color(self.todo_title, (1, 0, 0, 1), 'ti')
            self.title_error.text = 'Empty Title'
            err = 1

        if self.validate_task(self.start_date.text, 'date'):
            start_date = self.start_date.text
        else:
            self.reset_border_color(self.start_date, (1, 0, 0, 1), 'sd')
            self.sd_error.text = 'Invalid Format'
            f = 0
            start_date = ''
            err = 1

        if self.validate_task(self.start_time.text, 'time'):
            start_time = self.start_time.text
        else:
            self.reset_border_color(self.start_time, (1, 0, 0, 1), 'st')
            self.st_error.text = 'Invalid Format'
            f = 0
            start_time = ''
            err = 1

        if self.validate_task(self.end_date.text, 'date'):
            end_date = self.end_date.text
        else:
            self.reset_border_color(self.end_date, (1, 0, 0, 1), 'ed')
            self.ed_error.text = 'Invalid Format'
            f = 0
            end_date = ''
            err = 1

        if self.validate_task(self.end_time.text, 'time'):
            end_time = self.end_time.text
        else:
            self.reset_border_color(self.end_time, (1, 0, 0, 1), 'et')
            self.et_error.text = 'Invalid Format'
            f = 0
            end_time = ''
            err = 1

        start = ' '.join([start_date, start_time])
        end = ' '.join([end_date, end_time])

        if len(start) > 12:
            task['start'] = cal.datetime.datetime.strptime(start, '%d/%m/%Y %H:%M')
            self.task_id = self.task_id + task['start'].strftime('%d%m%Y%H%M') + '.'
        elif len(start) > 6:
            task['start'] = cal.datetime.datetime.strptime(start, '%d/%m/%Y ')
            self.task_id = self.task_id + task['start'].strftime('%d%m%Y') + 'xxxx.'
        elif len(start) > 3:
            self.reset_border_color(self.start_date, (1, 0, 0, 1), 'sd')
            if f:
                self.sd_error.text = 'Input Date'
                err = 1
        else:
            task['start'] = 0
            self.task_id = self.task_id + 'xxxxxxxxxxxxxx.'

        if len(end) > 12:
            task['end'] = cal.datetime.datetime.strptime(end, '%d/%m/%Y %H:%M')
            self.task_id = self.task_id + task['end'].strftime('%d%m%Y%H%M') + '.'
        elif len(end) > 6:
            task['end'] = cal.datetime.datetime.strptime(end, '%d/%m/%Y ')
            self.task_id = self.task_id + task['end'].strftime('%d%m%Y') + 'xxxx.'
        elif len(end) > 3:
            self.reset_border_color(self.end_date, (1, 0, 0, 1), 'ed')
            if f:
                self.ed_error.text = 'Input Date'
                err = 1
        else:
            task['end'] = 0
            self.task_id = self.task_id + 'xxxxxxxxxxxxxx.'

        if task['id'].startswith('AP'):

            if err != 1:
                if start_date == '':
                    err = 1
                    self.reset_border_color(self.start_date, (1, 0, 0, 1), 'sd')
                    self.sd_error.text = 'Set Date'
                if start_time == '':
                    err = 1
                    self.reset_border_color(self.start_time, (1, 0, 0, 1), 'st')
                    self.st_error.text = 'Set Time'

        if err:
            self.task_id = task['id']
            return

        self.task_id += self.priority.text

        task['id'] = self.task_id
        task['description'] = self.description.text
        self.on_submit(task)
        self.dismiss()

    def validate_task(self, text, data_type):
        if data_type == 'title':
            if len(text) == 0:
                return False
            else:
                return True

        if data_type == 'date':
            if len(text) != 0:
                try:
                    cal.datetime.datetime.strptime(text, '%d/%m/%Y')
                    return True
                except:
                    return False
            else:
                return True

        if data_type == 'time':
            if len(text) != 0:
                try:
                    cal.datetime.datetime.strptime(text, '%H:%M')
                    return True
                except:
                    return False
            else:
                return True

##########################################################################
###############                                            ###############
##########                       APP BUILD                      ##########
###############                                            ###############
##########################################################################

class ProductivityApp(MDApp):
    def build(self):
        self.root_layout = CustomBoxLayout()
        self.get_ids()

        return self.root_layout

    def get_ids(self):
        self.home_tab = self.root_layout.ids['home_tab']
        self.habit_tab = self.root_layout.ids['habit_tab']
        self.todo_tab = self.root_layout.ids['todo_tab']

ProductivityApp().run()