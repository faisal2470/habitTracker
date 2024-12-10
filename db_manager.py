import sqlite3


class DatabaseManager:
    def __init__(self, db_name='productivity_app.db'):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_name)
        else:
            pass