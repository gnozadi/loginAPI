from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
import time

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

lists = {"ali": "1234", "Mary": "qwerty", "admin": "password"}


@app.route("/", methods=['GET', 'POST'])
def home():
    session["attempts"] = 0
    now = time.time()
    session["firstLogin"] = now
    session["LastLogin"] = now
    session["timeBetween"] = 0
    session["limitReached"] = False
    return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    t = 0

    if request.method == 'POST':
        userID = request.form['username']
        userPass = request.form['password']
        if not session["limitReached"]:
            if userID not in lists.keys():
                error = "Wrong Credential"
                redirect(url_for("login"))
            elif userID in lists and lists[userID] != userPass:
                error = "Wrong Credential"
                session["attempts"] = session["attempts"] + 1
                # calculate time between attempts
                now = time.time()
                session["timeBetween"] = (now - session["LastLogin"] + session["timeBetween"])/session["attempts"]
                session["lastLogin"] = now
                t = session["timeBetween"] / 3600
                redirect(url_for("login"))
            if session["attempts"] > 5 and t < 1:
                session["limitReached"] = True

        else:
            return "You reached your limit.Try Again later"

    return render_template("login.html", error=error,)


if __name__ == "__main__":
    app.run(debug=True)
