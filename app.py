from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from email.message import EmailMessage
import ssl
import smtplib

from helpers import login_required


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///contact.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():

    user_id = session["user_id"]
    contact_info = db.execute("SELECT names, phone, email FROM contacts WHERE user_id = ?", user_id)

    return render_template("index.html", database = contact_info)


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()
    if request.method == "POST":

        if not request.form.get("username"):
            flash("MUST PROVIDE USERNAME")
            return redirect("/login")

        elif not request.form.get("password"):
            flash("MUST PROVIDE PASSWORD")
            return redirect("/login")

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("INVALID USERNAME OR PASSWORD")
            return redirect("/login")

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        remail = request.form.get("remail")
        rpassword = request.form.get("rpassword")


        if not username:
            flash("MUST HAVE USERNAME")
            return redirect("/register")

        if not password:
            flash("MUST HAVE PASSWORD!")
            return redirect("/register")

        if not confirmation:
            flash("MUST HAVE CONFIRMATION PASSWORD!")
            return redirect("/register")

        if password != confirmation:
            flash("PASSWORD AND CONFIRMATION PASSWORD DO NOT MATCH!")
            return redirect("/register")

        if not remail:
            flash("MUST HAVE EMAIL")
            return redirect("/register")

        if not rpassword:
            flash("MUST HAVE EMAIL PASSWORD")
            return redirect("/register")


        hash = generate_password_hash(password)

        try:
            new_user = db.execute("INSERT INTO users (username, hash, remail, rpassword) VALUES (?, ?, ?, ?)", username, hash, remail, rpassword)
        except:
            flash("USERNAME ALREADY EXISTS!")
            return redirect("/register")


        session["user_id"] = new_user
        return redirect("/")


@app.route("/contact", methods=["GET", "POST"])
@login_required
def contact():

    if request.method == "GET":
        return render_template("contact.html")

    else:
        names = request.form.get("names")
        phone = request.form.get("phone")
        email = request.form.get("email")

        if not names:
            flash("NEED A NAME")
            return redirect("/contact")

        if not phone:
            flash("NEED A PHONE NUMBER")
            return redirect("/contact")

        if not email:
            flash("NEED A EMAIL")
            return redirect("/contact")

        user_id = session["user_id"]
        db.execute("INSERT INTO contacts (names, phone, email, user_id) VALUES(?, ?, ?, ?)", names, phone, email, user_id)

        flash("Added Contact")
        return redirect("/contact")


@app.route("/email", methods=["GET", "POST"])
@login_required
def email():
    if request.method == "GET":
        return render_template("email.html")

    else:
        email = request.form.get("emails")
        subject = request.form.get("subject")
        body = request.form.get("body")


        user_id = session["user_id"]

        e = db.execute("SELECT remail FROM users WHERE id = :id", id=user_id)
        email_sender = e[0]["remail"]

        p = db.execute("SELECT rpassword FROM users WHERE id = :id", id=user_id)
        email_password = p[0]["rpassword"]


        email_receiver = email
        subject = subject
        body = body

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())


        flash("Email Sent")
        return redirect("/email")


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():

    if request.method == "GET":
        return render_template("delete.html")

    else:
        names = request.form.get("names")
        if not names:
            flash("NEED A NAME")
            return redirect("/delete")


        user_id = session["user_id"]
        db.execute("DELETE FROM contacts WHERE names = ? AND user_id = ?", names, user_id)

        flash("Deleted Contact")
        return redirect("/delete")