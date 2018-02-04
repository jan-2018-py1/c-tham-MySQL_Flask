from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = 'flaskRegistrationValidation'
mysql = MySQLConnector(app,'0emailsdb')

import re
# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


### Display all records

@app.route('/')
def index():
    print 'index'
    query = "SELECT id, email, date_format(created_at,'%m/%d/%Y %r') as created_at FROM emails"
    emails = mysql.query_db(query)
    return render_template('index.html', all_emails=emails)

### Display one record

@app.route('/<id>')
def show(id):
    print 'show'
    query = "SELECT id, email, date_format(created_at,'%m/%d/%Y %r') as created_at FROM emails"
    data = {
             'specific_id': id
           }
    emails = mysql.query_db(query, data)
    return render_template('index.html', all_emails=emails)

### Insert one record

@app.route('/', methods=['POST'])
def create():
    print 'insert'
    error = False
    email = request.form['email']
    print email
    #email
    if len(email) < 1:
        flash('** Your Email cannot be empty! **','error')
        error = True
    elif not EMAIL_REGEX.match(email):
        flash("** Invalid Email Address! **",'error')
        error = True
    if error == False:
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
        data = {
                'email': request.form['email']
            }
        mysql.query_db(query, data)
        flash('The email address you entered ('+email+') is a VALID email address! Thank you!','pass')
    return redirect('/')

### Update one record

@app.route('/update', methods=['POST'])
def update():
    print 'update'
    query = "UPDATE emails SET email = :email, updated_at = now() WHERE id = :id"
    data = {
             'email': request.form['email'],
             'id': request.form['id']
           }
    mysql.query_db(query, data)
    return redirect('/')

### Delete record

@app.route('/delete', methods=['POST'])
def delete():
    print 'delete'
    query = "DELETE FROM emails WHERE id = :id"
    data = {
            'id': request.form['id']
           }
    mysql.query_db(query, data)
    return redirect('/')

app.run(debug=True)
