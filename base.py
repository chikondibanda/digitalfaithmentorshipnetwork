import sqlite3
from hashlib import sha256
from datetime import datetime

class Database:
    def __init__(self, db_name='data.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            profile_pic TEXT DEFAULT 'https://placehold.co/150x150.png',
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS forums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS forum_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            forum_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (forum_id) REFERENCES forums (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS one_on_one_chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user1_id INTEGER NOT NULL,
            user2_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user1_id) REFERENCES users (id),
            FOREIGN KEY (user2_id) REFERENCES users (id)
        )
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (chat_id) REFERENCES one_on_one_chats (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        self.conn.commit()

    def hash_password(self, password):
        return sha256(password.encode()).hexdigest()

    def create_user(self, first_name, last_name, username, email, phone=None, profile_pic='https://placehold.co/150x150.png', password=None):
        password_hash = self.hash_password(password) if password else None
        created_at = datetime.now().isoformat()
        self.cursor.execute('''
        INSERT INTO users (first_name, last_name, username, email, phone, profile_pic, password_hash, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, username, email, phone, profile_pic, password_hash, created_at))
        self.conn.commit()

    def get_user(self, username):
        self.cursor.execute('''
        SELECT * FROM users WHERE username = ?
        ''', (username,))
        return self.cursor.fetchone()

    def get_user_by_email(self, email):
        self.cursor.execute('''
        SELECT * FROM users WHERE email = ?
        ''', (email,))
        return self.cursor.fetchone()

    def get_user_by_phone(self, phone):
        self.cursor.execute('''
        SELECT * FROM users WHERE phone = ?
        ''', (phone,))
        return self.cursor.fetchone()

    def update_user_profile_pic(self, username, profile_pic):
        self.cursor.execute('''
        UPDATE users
        SET profile_pic = ?
        WHERE username = ?
        ''', (profile_pic, username))
        self.conn.commit()

    def verify_password(self, email, password):
        user = self.get_user_by_email(email)
        if not user:
            return False
        return self.hash_password(password) == user[7]

    def close(self):
        self.conn.close()