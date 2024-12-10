import sqlite3

class DatabaseManager:
    def __init__(self, db_name='productivity_app.db'):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name)
        else:
            pass

    def create_tables(self):
        self.connect()
        self.cursor = self.conn.cursor()
        self.close()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
        else:
            pass

