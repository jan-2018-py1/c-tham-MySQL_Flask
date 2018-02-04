from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'0friendsdb')

### Main

@app.route('/')
def index():
    print '** main page'
    return redirect('/users')

### Display all records

@app.route('/users')
def showall():
    print '** show all users'
    query = "SELECT id, first_name, last_name, age, date_format(friend_since,'%M %e, %Y') as friend_since, date_format(created_at,'%M %e, %Y %r') as created_at, date_format(updated_at,'%M %e, %Y %r') as updated_at FROM friends"
    db = mysql.query_db(query)
    return render_template('index.html', all_friends=db, key=0)

### Display one record

@app.route('/users/<friend_id>')
def showone(friend_id):
    print '** show one user'
    query = "SELECT id, first_name, last_name, age, date_format(friend_since,'%M %e, %Y') as friend_since, date_format(created_at,'%M %e, %Y %r') as created_at, date_format(updated_at,'%M %e, %Y %r') as updated_at FROM friends WHERE id = :specific_id"
    data = {
             'specific_id': friend_id
           }
    db = mysql.query_db(query, data)
    return render_template('index.html', all_friends=db, key=1)

### Insert one record

@app.route('/users/new')
def showadd():
    print 'show insert page'
    return render_template('add.html')

@app.route('/add', methods=['POST'])
def add():
    print 'insert a record'
    query = "INSERT INTO friends (first_name, last_name, age, friend_since, created_at, updated_at) VALUES (:first_name, :last_name, :age, :friend_since, NOW(), NOW())"
    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'age': request.form['age'],
             'friend_since': request.form['friend_since']
           }
    mysql.query_db(query, data)
    return redirect('/users')

### Update one record

@app.route('/users/<friend_id>/edit')
def showupdate(friend_id):
    print '** show one user'
    query = "SELECT id, first_name, last_name, age, date_format(friend_since,'%Y-%m-%d') as friend_since FROM friends WHERE id = :specific_id"
    data = {
             'specific_id': friend_id
           }
    db = mysql.query_db(query, data)
    return render_template('update.html',all_friends=db[0])

@app.route('/update', methods=['POST'])
def update():
    print '** update one user'
    query = "UPDATE friends SET first_name = :one, last_name = :two, age = :three, friend_since = :four, updated_at = now() WHERE id = :five"
    data = {
             'one': request.form['first_name'],
             'two':  request.form['last_name'],
             'three': request.form['age'],
             'four': request.form['friend_since'],
             'five': request.form['userID']
           }
    mysql.query_db(query, data)
    return redirect('/users')

### Delete record

@app.route('/users/<friend_id>/destory')
def showdelete(friend_id):
    print '** show one user'
    query = "SELECT id, first_name, last_name, age, date_format(friend_since,'%M %e, %Y') as friend_since, date_format(created_at,'%M %e, %Y %r') as created_at, date_format(updated_at,'%M %e, %Y %r') as updated_at FROM friends WHERE id = :specific_id"
    data = {
             'specific_id': friend_id
           }
    db = mysql.query_db(query, data)
    return render_template('delete.html', all_friends=db)

@app.route('/delete', methods=['POST'])
def delete():
    print '** delete one user'
    query = "DELETE FROM friends WHERE id = :id"
    data = {
            'id': request.form['userID']
           }
    mysql.query_db(query, data)
    return redirect('/')

app.run(debug=True)
