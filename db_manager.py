import sqlite3

class DatabaseManager:
    def __init__(self, db_name='productivity_app.db'):
        self.db_name = db_name
        self.conn = None
        self.connect()
        self.close()

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name)
        else:
            pass

    def create_tables(self):
        self.connect()
        cursor = self.conn.cursor()
#         cursor.execute('''CREATE TABLE IF NOT EXISTS Todo (
#                        id TEXT PRIMARY KEY
#                        name TEXT NOT NULL
#                        )
# '''

#         )
        self.close()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
        else:
            pass

dbm = DatabaseManager()