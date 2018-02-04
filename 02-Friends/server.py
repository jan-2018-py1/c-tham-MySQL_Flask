from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'0friendsdb')

### Display all records

@app.route('/')
def index():
    print 'index'
    query = "SELECT id, first_name, last_name, age, date_format(friend_since,'%M %e, %Y') as friend_since FROM friends"
    friends = mysql.query_db(query)
    return render_template('index.html', all_friends=friends)

### Display one record

@app.route('/friends/<friend_id>')
def show(friend_id):
    print 'show'
    query = "SELECT id, first_name, last_name, age, date_format(friend_since,'%M %e, %Y') as friend_since FROM friends WHERE id = :specific_id"
    data = {
             'specific_id': friend_id
           }
    friends = mysql.query_db(query, data)
    return render_template('index.html', all_friends=friends)

### Insert one record

@app.route('/friends', methods=['POST'])
def create():
    print 'insert'
    query = "INSERT INTO friends (first_name, last_name, age, friend_since, created_at, updated_at) VALUES (:first_name, :last_name, :age, :friend_since, NOW(), NOW())"
    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'age': request.form['age'],
             'friend_since': request.form['friend_since']
           }
    mysql.query_db(query, data)
    return redirect('/')

### Update one record

@app.route('/update', methods=['POST'])
def update():
    print 'update'
    query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, age = :age, friend_since = :friend_since, updated_at = now() WHERE id = :id"
    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'age': request.form['age'],
             'friend_since': request.form['friend_since'],
             'id': request.form['id']
           }
    mysql.query_db(query, data)
    return redirect('/')

### Delete record

@app.route('/delete', methods=['POST'])
def delete():
    print 'delete'
    query = "DELETE FROM friends WHERE id = :id"
    data = {
            'id': request.form['id']
           }
    mysql.query_db(query, data)
    return redirect('/')

app.run(debug=True)
