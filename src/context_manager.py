import sqlite3

def initialize_db():
    conn = sqlite3.connect('context.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS context_history (
                        id INTEGER PRIMARY KEY,
                        context TEXT
                    )''')
    conn.commit()
    conn.close()

def save_context(context):
    conn = sqlite3.connect('context.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO context_history (context) VALUES (?)", (context,))
    conn.commit()
    conn.close()

def load_context():
    conn = sqlite3.connect('context.db')
    cursor = conn.cursor()
    cursor.execute("SELECT context FROM context_history ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else ""
