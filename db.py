import sqlite3
import hashlib

class SecurityHandler:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('users.db')
            self.create_users_table()
        except sqlite3.Error as e:
            print(e)

    def create_users_table(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

    def create_user(self, username, password):
        c = self.conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        c.execute('INSERT INTO users VALUES (?, ?)', (username, hashed_password))
        self.conn.commit()
        print("User created successfully")

    def login_user(self, username, password):
        c = self.conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
        user = c.fetchone()
        return user is not None

    def reset_database(self):
        print("Resetting the database")
        c = self.conn.cursor()
        c.execute('DROP TABLE users')
        self.create_users_table()
        self.close_connection()



def create_teams_table():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                code TEXT NOT NULL
        )
        ''')
    
    id = 0
    name = "celtics"
    code = 'CEL'

    #for loop iterating through csv and cosnstantly adding values into table
    c.execute('INSERT INTO teams VALUES (?, ?, ?)', (id, name, code))
    conn.commit()
    print(f"SELECT * FROM teams WHERE code=\'{code}\'")

    c.execute(f"SELECT * FROM teams WHERE code=\'{code}\'")

    
    x = c.fetchone()

    print(x[1])

if __name__ == '__main__':
    create_teams_table()

    



    