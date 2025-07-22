import sqlite3

def save_to_history(question, answer):
    conn = sqlite3.connect("history.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS history (question TEXT, answer TEXT)''')
    cur.execute("INSERT INTO history (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect("history.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM history ORDER BY rowid DESC LIMIT 10")
    rows = cur.fetchall()
    conn.close()
    return rows
