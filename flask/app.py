# Standard Library Imports
import os
import sqlite3
from os import urandom
from dotenv import load_dotenv

# Third-Party Imports
from flask import Flask, jsonify, render_template, redirect, request, session, url_for, g

# External Library Imports
import google.generativeai as genai
from google.auth import load_credentials_from_file
from google.oauth2 import credentials
from google.auth.transport.requests import Request
from google.generativeai import generative_models


app = Flask(__name__)
app.secret_key = urandom(24)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
load_dotenv()
DATABASE = 'task.db'
app.config['DATABASE'] = DATABASE

genai_client = None

try:
    api_key = os.getenv("GENAI_API_KEY")
    if api_key:
        genai_client = generative_models.GenerativeModelsServiceClient(api_key=api_key)
    else:
        print("GENAI_API_KEY environment variable is not set.")
except Exception as e:
    print("Error initializing GenAI client:", e)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf-8'))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Ensure required fields are filled
        if (
            not request.form.get("email")
            or not request.form.get("passw")
            or not request.form.get("first_name")
            or not request.form.get("last_name")
        ):
            return render_template("error.html")

        email = request.form.get("email")
        passw = request.form.get("passw")
        first_name = request.form.get("first_name")
        first_name = first_name[0].upper() + first_name[1:]
        last_name = request.form.get("last_name")
        last_name = last_name[0].upper() + last_name[1:]


        db = get_db()
        cursor = db.cursor()
       # print("Email:", email)

        # Check if email already exists in the database
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return render_template("error.html")

        # Insert the new user into the database
        cursor.execute(
            "INSERT INTO users (first_name, last_name, email, passw) VALUES (?, ?, ?, ?)",
            (first_name, last_name, email, passw),
        )
        db.commit()

        # Retrieve the inserted user's ID
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        user_id = cursor.fetchone()[0]

# Store user ID in the session
        session["user_id"] = user_id

        return redirect(url_for("home"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        passw = request.form.get("passw")  # Rename to "password" for clarity
        print(email)
        print(passw)
        db = get_db()
        cursor = db.cursor()

        # Retrieve the user's record from the database based on email
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if not user:
            return render_template("error.html")

        # Compare the provided password with the password stored in the database
        if user[4] == passw:  # Assuming both are plain text
            # Store user information in the session
            session["user_id"] = user[0]
            return redirect(url_for("home"))
        else:
            return render_template("error.html")

    return render_template("login.html")


def generate_scheduling_query(tasks):
    query = "In the format of datetime(SQL QUERY FORMAT) start, datetime end and return a list of the best way the schedule these tasks today. Assume the person is working a 9 to 5 so everything either be before 9 or after 5. Each task will either be around an hour.\n:"
    taskss =""
    for task in tasks:
        taskss+=f"SCHEDULE TASK:'{task}'\n"
    model = genai.GenerativeModel('models/gemini-pro')
    result = model.generate_content(query + taskss)
    return result

@app.route("/taskschedule", methods=["GET", "POST"])
def taskschedule():
    if request.method == "POST":
        data = request.json  # Extract the JSON data sent from the frontend
        tasks = data.get("tasks")  # Extract the "tasks" list from the JSON data
        # Process the tasks data here
        print("Received tasks:", tasks)
        # Optionally, you can store the tasks in a database or perform 
        stripTasks = []
        for i in tasks:
            i = i.replace('Delete Task', '')
            stripTasks.append(i)
        print("Modified tasks:", stripTasks)
        query_result = generate_scheduling_query(stripTasks)
        content = query_result.text
        # Construct response message
        response = {
            "content": content
        }
        print(content)
        return jsonify(response)
    else:
        return render_template("taskschedule.html")
   
@app.route('/home') 
def home():
    return render_template("home.html")
    
@app.route('/')
def index():
    return redirect(url_for('home'))

init_db()
if __name__ == "__main__":
    app.run(debug=True)

