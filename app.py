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

@app.route("/")
def index():
    return render_template("signup.html")

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

        # Store user information in the session
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        session["user_id"] = user["id"]

        return redirect(url_for("mainpage"))

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
        if user["passw"] == passw:  # Assuming both are plain text
            # Store user information in the session
            session["user_id"] = user["id"]
            return redirect(url_for("mainpage"))
        else:
            return render_template("error.html")

    return render_template("login.html")


init_builtin()
if __name__ == "__main__":
    app.run(debug=True)
