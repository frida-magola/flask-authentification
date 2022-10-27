import functools
from flask import (
  Flask,
  session,
  render_template,
  request,
  abort,
  flash,
  redirect,
  url_for
) 

from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.secret_key = 'xwALPgXfYX-W06pnxdehS2VFlDT9vIxBZVuzWULICVk'

users = {}


def login_required(route):
  @functools.wraps(route)
  def route_wrapper(*args, **kwargs):
    # email = session.get("email")
    if not session.get("email"):
      return redirect(url_for("login"))
    return route(*args, **kwargs)
  return route_wrapper

@app.route('/')
@login_required
def home():
  return render_template("home.html", email=session.get("email"))

@app.route("/protected")
@login_required
def protected():
  return render_template("protected.html",email=session.get("email"))


@app.route("/login", methods=["GET", "POST"])
def login():
  email = ""
  
  if request.method == "POST":
    email = request.form.get("email")
    password = request.form.get("password")
    
    if pbkdf2_sha256.verify(password, users.get(email)):
      session["email"] = email
      return redirect(url_for("protected"))
    flash("Incorrect e-mail or password.")
    
  return render_template("login.html", email=email)


@app.route("/signup", methods=["GET", "POST"])
def signup():
  
  if request.method == "POST":
    email = request.form.get("email")
    password = request.form.get("password")
    #validation data
    #verify email after sign up
    #temporary story user in users dictionnary
    users[email] = pbkdf2_sha256.hash(password) 
    # print(users)
    #store data in session
    session["email"] = email
    flash("you're successfully sign up")
    return redirect(url_for("login"))
  
  return render_template("signup.html")


@app.route("/logout", methods=["POST"])
def logout():
   
  if request.method == "POST":
    email = request.form.get('email')
    
    if session.get("email") == email:
      
      session.clear()
      return redirect(url_for("home"))



