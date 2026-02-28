from flask import Flask, redirect, request, session, url_for
from flask import render_template

from db import db_connector

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
    message = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # SQL Injection Query
        query = f"SELECT id, username FROM users WHERE username='{username}' AND password='{password}'"

        connector = db_connector()
        cursor = connector.cursor()
        
        cursor.execute(query)
        row = cursor.fetchone()
        
        cursor.close()
        connector.close()

        if row:
            session["user"] = row[1]
            return redirect(url_for("homepage"))
        else:
            message = "Invalid credentials"

    return render_template("login.html", msg=message)

@app.route("/homepage")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("homepage.html", username=session["user"])

if __name__ == "__main__":
    app.run(debug=True)