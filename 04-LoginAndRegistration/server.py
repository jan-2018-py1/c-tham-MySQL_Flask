from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'flaskRegistrationValidation'
mysql = MySQLConnector(app,'0loginregistration')

import re
# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]')
PASSWORD_REGEX = re.compile(r'^[A-Z].*\d|\d.*[A-Z]') 
DOB_REGEX = re.compile(r'19|20[0-9]{2}-[0-9]{2}-[0-9]{2}')
# A-Z, any char with 0 or more, digit  or  digit, any char with 0 or more, A-Z

import os, binascii, md5 # include this at the top of your file
salt = binascii.b2a_hex(os.urandom(15))

####################
@app.route('/')
def index():
  print "** index **"
  return render_template('index.html')

####################
@app.route('/registration',methods=['POST'])
def registration():
  print "** registration **"
  error = False
  today = str(datetime.now())[:10]
  print 'today is '+today
  email = request.form['email']
  firstname = request.form['firstname']
  lastname = request.form['lastname']
  password1 = request.form['password1']
  password2 = request.form['password2']
  dob = request.form['dob']
  print '* ',email, firstname, lastname, password1, password2, dob
#email
  if len(email) < 1:
    flash('** Your Email cannot be empty! **','error_empty')
    error = True
  elif not EMAIL_REGEX.match(email):
    flash("** Invalid Email Address! **",'error_invalid')
    error = True
#first name
  if len(firstname) < 1:
    flash('** Your First Name cannot be empty! **','error_empty')
    error = True
  elif len(firstname) < 2:
    flash('** Your First Name should be more than 2 characters! **','error_invalid')
    error = True
  elif not NAME_REGEX.match(firstname):
    flash('** Your First Name cannot contain any numbers! **',"error_invalid")
    error = True
#last name
  if len(lastname) < 1:
    flash('** Your Last Name cannot be empty! **','error_empty')
    error = True
  elif len(lastname) < 2:
    flash('** Your Last Name should be more than 2 characters! **','error_invalid')
    error = True
  elif not NAME_REGEX.match(lastname):
    flash('** Your Last Name cannot contain any numbers! **',"error_invalid")
    error = True
#password
  if len(password1) < 1:
    flash('** Your Password cannot be empty! **','error_empty')
    error = True 
  elif len(password1) < 8:
    flash('** Your Password should be more than 8 characters **','error_invalid')
    error = True
  elif not PASSWORD_REGEX.match(password1):
    flash('** A password to have at least 1 uppercase letter and 1 numeric value **','error_ninja')
    error = True
#confirm password
  if len(password2) < 1:
    flash('** A confirm password cannot be empty! **','error_empty')
    error = True
  elif len(password2) < 8:
    flash('** Your confirm password should be more than 8 characters **','error_invalid')
    error = True
  elif not PASSWORD_REGEX.match(password2):
    flash('** A confirm password to have at least 1 uppercase letter and 1 numeric value **','error_ninja')
    error = True
#match password
  if password1 != password2:
    flash('** Password and password confirmation should match! **','error_invalid')
    error = True
#date of birth
  if len(dob) < 1:
    flash('** Your date of birth cannot be empty! **','error_hacker')
    error = True
  elif not DOB_REGEX.match(dob):
    flash('** Your date of birth is invalid! **','error_hacker')
    error = True
  elif str(dob) > today:
    flash('** Your date of birth must be from the past! **','error_hacker')
    error = True
#others
  if error == False:
# check duplicate email address
    print "** check duplicate email **"
    query = "SELECT * FROM users WHERE email_address = :first"
    data = {
             'first': email
           }
    x1 = mysql.query_db(query, data)
    print x1
    if len(x1) > 0:
      flash('** Your email address ('+email+') is already registrated **','error_hacker')
      flash('** Please enter a different email address **','error_hacker')
      error = True
      return redirect('/')
#insert database
    print "** insert **"
    hashed_pw = md5.new(password1 + salt).hexdigest()
    query = "INSERT INTO users (`first_name`, `last_name`, `email_address`, `password`, `dob`, `created_at`, `updated_at`) VALUES (:first, :second, :third, :forth, :fifth, now(), now())"
    data = {
             'first': firstname,
             'second': lastname,
             'third': email,
            #  'forth': password1,
             'forth': hashed_pw,
             'fifth': str(dob)
           }
    x2 = mysql.query_db(query, data)
    print x2
    if len(str(x2)) > 0:
      flash('Thanks for submitting your information.','pass')
      flash(str('('+email+') ('+firstname+') ('+lastname+') ('+password1+')  ('+hashed_pw+') ('+dob+')'),'pass')
      session["user_id"] = x2
      return redirect("/dashboard")
    else:
      flash('** System Error. Uunable to insert record **','error_hacker')
  return redirect('/')

####################
@app.route('/login',methods=['POST'])
def login():
  print "** login **"
  error = False
  email = request.form['email']
  password = request.form['password']
#email
  if len(email) < 1:
    flash('** Your Email cannot be empty! **','error_empty')
    error = True
  elif not EMAIL_REGEX.match(email):
    flash("** Invalid Email Address! **",'error_invalid')
    error = True
#password
  if len(password) < 1:
    flash('** Your Password cannot be empty! **','error_empty')
    error = True 
#others
  if error == False:
# check duplicate email address
    print "** velifying **"
    query = "SELECT * FROM users WHERE email_address = :first and password = :second"
    data = {
             'first': email,
             'second': md5.new(password + salt).hexdigest()
           }
    x3 = mysql.query_db(query, data)
    print x3
    if len(x3) == 0:
      flash('** Your email address or/and password are incorrected **','error_hacker')
      error = True
    else:
      flash('Thanks for submitting your information.','pass')
      session["user_id"] = x3[0]["id"]
      print session["user_id"]
      return redirect("/dashboard")
  return redirect('/')

####################
@app.route("/dashboard")
def dashboard():
  print "** dashboard **"
  print session["user_id"]
  # return render_template("dashboard.html")
  query = "SELECT * FROM users WHERE id = :first"
  data = {
          "first": session["user_id"]
        }
  x4 = mysql.query_db(query, data) #list of dictionaries
  print x4
  return render_template("dashboard.html", user = x4[0])

####################
@app.route("/logout")
def logout():
  print "** logout **"
  session.clear()
  return redirect("/")

####################
app.run(debug=True)
