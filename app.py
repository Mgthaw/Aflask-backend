from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

# Database Initialize
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            balance INTEGER DEFAULT 0,
            role TEXT DEFAULT "user"
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return "Mobile Legends Diamond Shop Backend is Running"

@app.route("/register", methods=['POST'])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    hashed_pw = generate_password_hash(password)

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_pw, "user"))
        conn.commit()
        return "Registered successfully!"
    except sqlite3.IntegrityError:
        return "Username already exists."
    finally:
        conn.close()

@app.route("/login", methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()

    if row and check_password_hash(row[0], password):
        return "Login success!"
    else:
        return "Invalid credentials."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
