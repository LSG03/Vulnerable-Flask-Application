from flask import Flask, redirect, request, session, url_for
from flask import render_template

from db import db_connector

app = Flask(__name__)

app.secret_key = "key"

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # SQL Injection Query
        query = f"SELECT id, username, password FROM users WHERE username='{username}'"

        connector = db_connector()
        cursor = connector.cursor()
        
        cursor.execute(query)
        row = cursor.fetchone()
        
        cursor.close()
        connector.close()

        if row and row[2] == password:
            session["user"] = row[1]
            return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/homepage")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("homepage.html", username=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)