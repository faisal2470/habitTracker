import sqlite3

class DatabaseManager:
    def __init__(self, db_name='productivity_app.db'):
        self.db_name = db_name
        self.conn = None
        self.connect()
        self.create_tables()
        self.close()

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name)
        else:
            pass

    def create_tables(self):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Todo (
                       id TEXT PRIMARY KEY,
                       name TEXT NOT NULL,
                       priority INT NOT NULL,
                       status REAL NOT NULL,
                       start_date TEXT,
                       start_time TEXT,
                       end_date TEXT,
                       end_time TEXT,
                       desc TEXT,
                       subtasks TEXT
                       )''')
        self.conn.commit()
        self.close()

    def insert_todo(self, task):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM Todo WHERE id LIKE ?', (task['id'] + '%',))
        todo_list = cursor.fetchall()
        if len(todo_list):
            print('Not Empty')
            print(todo_list)
            self.close()
            return
        else:
            task['id'] += '.0'
            print(task['id'], todo_list)

        if task['start']:
            start_date = task['start'].strftime('%d/%m/%Y')
            if 'x' in task['id'].split('.')[1]:
                start_time = ''
            else:
                start_time = task['start'].strftime('%H:%M')
        else:
            start_date = ''
            start_time = ''

        if task['end']:
            end_date = task['end'].strftime('%d/%m/%Y')
            if 'x' in task['id'].split('.')[2]:
                end_time = ''
            else:
                end_time = task['end'].strftime('%H:%M')
        else:
            end_date = ''
            end_time = ''

        for ind, val in enumerate(['N', 'L', 'M', 'H']):
            if task['id'].split('.')[-2] == val:
                priority = ind

        cursor.execute('INSERT INTO Todo VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (task['id'], task['title'], priority, 0, start_date, start_time, end_date, end_time, task['desc'], ''))
        self.conn.commit()
        self.close()


    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
        else:
            pass

dbm = DatabaseManager()