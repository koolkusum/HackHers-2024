from imp import init_builtin
from os import urandom
from flask import Flask, render_template, redirect, request, session, url_for
import sqlite3
import google.generativeai as genai


app = Flask(__name__)
app.secret_key = urandom(24)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

DATABASE = 'task.db'


from os import urandom
from flask import Flask, render_template, request, jsonify, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = urandom(24)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

DATABASE = 'task.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            task TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/")
def index():
    init_db()
    return render_template("mainpage.html")

