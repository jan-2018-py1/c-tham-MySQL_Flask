from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'theWallsEcrEtkEy'
mysql = MySQLConnector(app,'0wall')

import re
# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]')
PASSWORD_REGEX = re.compile(r'^[A-Z].*\d|\d.*[A-Z]') 
DOB_REGEX = re.compile(r'19|20[0-9]{2}-[0-9]{2}-[0-9]{2}')
# A-Z, any char with 0 or more, digit  or  digit, any char with 0 or more, A-Z

import os, binascii # include this at the top of your file
# salt = binascii.b2a_hex(os.urandom(15))
salt = binascii.b2a_hex(app.secret_key)

import md5
import time

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
  print 'Input fields-',email, firstname, lastname, password1, password2, dob
#email
  if len(email) < 1:
    flash('** (Registration) Your Email cannot be empty! **','error_empty')
    error = True
  elif not EMAIL_REGEX.match(email):
    flash("** (Registration) Invalid Email Address! **",'error_invalid')
    error = True
#first name
  if len(firstname) < 1:
    flash('** (Registration) Your First Name cannot be empty! **','error_empty')
    error = True
  elif len(firstname) < 2:
    flash('** (Registration) Your First Name should be more than 2 characters! **','error_invalid')
    error = True
  elif not NAME_REGEX.match(firstname):
    flash('** (Registration) Your First Name cannot contain any numbers! **',"error_invalid")
    error = True
#last name
  if len(lastname) < 1:
    flash('** (Registration) Your Last Name cannot be empty! **','error_empty')
    error = True
  elif len(lastname) < 2:
    flash('** (Registration) Your Last Name should be more than 2 characters! **','error_invalid')
    error = True
  elif not NAME_REGEX.match(lastname):
    flash('** (Registration) Your Last Name cannot contain any numbers! **',"error_invalid")
    error = True
#password
  if len(password1) < 1:
    flash('** (Registration) Your Password cannot be empty! **','error_empty')
    error = True 
  elif len(password1) < 8:
    flash('** (Registration) Your Password should be more than 8 characters **','error_invalid')
    error = True
  elif not PASSWORD_REGEX.match(password1):
    flash('** (Registration) A password to have at least 1 uppercase letter and 1 numeric value **','error_ninja')
    error = True
#confirm password
  if len(password2) < 1:
    flash('** (Registration) A confirm password cannot be empty! **','error_empty')
    error = True
  elif len(password2) < 8:
    flash('** (Registration) Your confirm password should be more than 8 characters **','error_invalid')
    error = True
  elif not PASSWORD_REGEX.match(password2):
    flash('** (Registration) A confirm password to have at least 1 uppercase letter and 1 numeric value **','error_ninja')
    error = True
#match password
  if password1 != password2:
    flash('** (Registration) Password and password confirmation should match! **','error_invalid')
    error = True
#date of birth
  if len(dob) < 1:
    flash('** (Registration) Your date of birth cannot be empty! **','error_hacker')
    error = True
  elif not DOB_REGEX.match(dob):
    flash('** (Registration) Your date of birth is invalid! **','error_hacker')
    error = True
  elif str(dob) > today:
    flash('** (Registration) Your date of birth must be from the past! **','error_hacker')
    error = True
#others
  if error == False:
# check duplicate email address
    print "** check duplicate email **"
    query = "SELECT * FROM users WHERE email_address = :first"
    data = {
             'first': email
           }
    db = mysql.query_db(query, data)
    # print db
    if len(db) > 0:
      flash('** (Registration) Your email address ('+email+') is already registrated **','error_hacker')
      flash('** (Registration) Please enter a different email address **','error_hacker')
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
             'forth': hashed_pw,
             'fifth': str(dob)
           }
    db = mysql.query_db(query, data)
    # print db
    if len(str(db)) > 0:
      flash('Account created successfull.','pass')
      flash(str('('+email+') ('+firstname+') ('+lastname+') ('+password1+')  ('+hashed_pw+') ('+dob+') ('+salt+') '),'error_hacker')
      session["user_id"] = db
      return redirect("/dashboard")
    else:
      flash('** (Registration) System Error. Uunable to insert record **','error_hacker')
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
    flash('** (Login) Your Email cannot be empty! **','error_empty')
    error = True
  elif not EMAIL_REGEX.match(email):
    flash("** (Login) Invalid Email Address! **",'error_invalid')
    error = True
#password
  if len(password) < 1:
    flash('** (Login) Your Password cannot be empty! **','error_empty')
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
    db = mysql.query_db(query, data)
    # print db
    # print md5.new(password + salt).hexdigest()
    # print salt
    if len(db) == 0:
      flash('** (Login) Your email address or/and password are incorrected **','error_hacker')
      error = True
    else:
      flash('Login successful.','pass')
      session["user_id"] = db[0]["id"]
      print "User ID-",session["user_id"]
      return redirect("/dashboard")
  return redirect('/')

####################
@app.route("/dashboard")
def dashboard():
  print "** dashboard **"
  print "User ID-",session["user_id"]
  # return render_template("dashboard.html")
  print "** message **"
  query = "SELECT * FROM users WHERE id = :first"
  data = {
          "first": session["user_id"]
        }
  db1 = mysql.query_db(query, data) #list of dictionaries
  # print db1
  query = "select m.id, m.user_id, concat(u.first_name,' ',u.last_name) as name, m.message, date_format(m.created_at,'%M %D %Y, %r') as created_at, m.created_at as messageDatetime from messages m join users u on m.user_id = u.id order by m.created_at desc"
  db2 = mysql.query_db(query) #list of dictionaries
  # print db2
  #-----
  print "** comments **"
  query = "select c.id, c.user_id, c.message_id, concat(u.first_name,'  ',u.last_name) as name, c.comment, date_format(c.created_at,'%M %D %Y, %r') as created_at from comments c left join messages m on c.message_id = m.id left join users u on c.user_id = u.id order by c.created_at desc"
  db3 = mysql.query_db(query)
  # print db3
  #-----
  return render_template("dashboard.html", user=db1[0], postmessage=db2, postcomment=db3)

####################
@app.route("/postmessage",methods=['POST'])
def message():
  print "** post message **"
  print "User ID-",session["user_id"]
  message = request.form['message']
  # print message
  if len(message) == 0:
    flash('** Your message is empty **','error_hacker')
  else:
    query = "INSERT INTO messages (`user_id`, `message`, `created_at`, `updated_at`) VALUES (:first, :second, now(), now())"
    data = {
             'first': session["user_id"],
             'second': message
           }
    db = mysql.query_db(query, data)
    # print db
    if len(str(db)) > 0:
      flash('Message posted succesful.','pass')
    else:
      flash('** System Error. Unable to post a message **','error_hacker')
  return redirect("/dashboard")

####################
@app.route("/postcomment",methods=['POST'])
def comment():
  print "** post comment **"
  print "User ID-",session["user_id"]
  print "Message ID-",request.form['messageID']
  comment = request.form['comment']
  # print comment
  if len(comment) == 0:
    flash('** Your comment is empty **','error_hacker')
  else:
    query = "INSERT INTO comments (`user_id`, `message_id`, `comment`, `created_at`, `updated_at`) VALUES (:first, :second, :third, now(), now())"
    data = {
             'first': session["user_id"],
             'second': request.form['messageID'],
             'third': comment
           }
    db = mysql.query_db(query, data)
    # print db
    if len(str(db)) > 0:
      flash('Comment posted succesful.','pass')
    else:
      flash('** System Error. Unable to post a comment **','error_hacker')
  return redirect("/dashboard")

####################
@app.route("/deletemessage",methods=['POST'])
def deletemessage():
  waitMinute = 3
  print "*** delete my message ***"
  print "User ID-",session["user_id"]
  print "Message ID-",request.form['messageID']
  d1 = request.form['messageDatetime']
  d2 = str(datetime.now())[:19]
  print "Message time-", d1, "Current time-", d2
  dd1 = time.mktime(time.strptime(d1, '%Y-%m-%d %H:%M:%S'))
  dd2 = time.mktime(time.strptime(d2, '%Y-%m-%d %H:%M:%S'))
  dd = (dd2 - dd1) / 60
  print "Time Diff in minute(s)-", dd
  if dd > waitMinute:
    # Delete comment(s) first
    print "Delete from comment table"
    query = "DELETE FROM `comments` WHERE `message_id`=:first"
    data = {
              'first': request.form['messageID']
    }
    db = mysql.query_db(query, data)
    print db
    if len(str(db)) > 0:
      flash('Comment(s) deleted succesful.','pass')
    else:
      flash('** System Error. Unable to delete comment(s) **','error_hacker')
    # Delete message second
    print "Delete from message table"
    query = "DELETE FROM `messages` WHERE `user_id`=:first and `id`=:second"
    data = {
              'first': session["user_id"],
              'second': request.form['messageID']
    }
    db = mysql.query_db(query, data)
    print db
    if len(str(db)) > 0:
      flash('Message deleted succesful.','pass')
    else:
      flash('** System Error. Unable to delete message **','error_hacker')
  else:
    flash('** You must wait '+str(waitMinute)+' minutes in order to delete your message. **', 'error_hacker')
  return redirect("/dashboard")

####################
@app.route("/logout")
def logout():
  print "** logout **"
  session.clear()
  flash('Logout succesful.','pass')
  return redirect("/")

####################
app.run(debug=True)
