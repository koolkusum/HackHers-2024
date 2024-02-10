from os import urandom
from flask import Flask, render_template, redirect, request, session, url_for
import sqlite3
import google.generativeai as genai


app = Flask(__name__)
app.secret_key = urandom(24)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

DATABASE = 'task.db'

@app.route("/")
def index():
    return render_template("signup.html")

