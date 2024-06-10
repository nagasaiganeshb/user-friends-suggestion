
import sqlite3


DATABASE_URL = 'friends.db'

def initialize_db():
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS friendships (
            user_id INTEGER,
            friend_id INTEGER,
            PRIMARY KEY (user_id, friend_id)
        );
        
        CREATE TABLE IF NOT EXISTS friend_suggestions (
            user_id INTEGER,
            suggested_friend_id INTEGER,
            PRIMARY KEY (user_id, suggested_friend_id)
        );
    """)

    cursor.executescript("""
        INSERT OR IGNORE INTO users (user_id, username) VALUES
            (1, 'User1'),
            (2, 'User2'),
            (3, 'User3'),
            (4, 'User4'),
            (5, 'User5');

        INSERT OR IGNORE INTO friendships (user_id, friend_id) VALUES
            (1, 2),
            (1, 3),
            (2, 1),
            (2, 4),
            (3, 1),
            (3, 5),
            (4, 2),
            (5, 3);
    """)

    conn.commit()
    conn.close()


def get_db_connection():
    """
    Establish and return a database connection.
    
    Returns:
        sqlite3.Connection: SQLite3 connection object.
    """
    return sqlite3.connect(DATABASE_URL)
