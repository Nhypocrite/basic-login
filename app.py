from flask import Flask, render_template, redirect, url_for, request, jsonify, session, g
from flask_cors import CORS
import mysql.connector
import hashlib
import random
import os
from datetime import timedelta

app = Flask(__name__)
CORS(app)

# Set secret_key for session encryption
app.secret_key = os.urandom(24)

# Configure database connection
db_config = {
    "user": "root",
    "password": "",
    "host": "localhost",
    "database": "web_programming",
    "charset": "utf8mb4",
    "collation": "utf8mb4_general_ci",
}

# Set session expiration time
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)


# Optimization: Use the g object to store the database connection to avoid creating a new connection on each request
# Get database connection
def get_db():
    if "db" not in g:
        g.db = mysql.connector.connect(**db_config)
    return g.db


# Close database connection
@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# Password encryption function
def hash_password(password):
    salt = "NTUSALT1234"
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()


# Register user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        encrypted_password = hash_password(request.form["password"])

        # Insert user data into the database
        try:
            connection = get_db()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, encrypted_password))
            connection.commit()
            cursor.close()
            return redirect(url_for("login"))
        except mysql.connector.IntegrityError:  # Username already exists
            return "Username already exists.", 400
        except mysql.connector.Error as err:
            return "An error occurred. Please try again later.", 500
    return render_template("register.html")


# Log in user
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        encrypted_password = hash_password(request.form["password"])

        # Get database connection and search for the user
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        # Verify password
        if user and user[2] == encrypted_password:

            session["user_id"] = user[0]
            session["username"] = user[1]

            # Handle "Remember me" functionality
            if request.form.get("remember_me"):
                session.permanent = True  # Enable persistent session (saved for 7 days as set above)
            else:
                session.permanent = False  # Enable short-lived session (expires when the browser is closed)

            return redirect(url_for("index"))

        cursor.close()

    return render_template("login.html")


# Log out user
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect(url_for("login"))


# Home page
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", username=session["username"])


if __name__ == "__main__":
    app.run(debug=True)
