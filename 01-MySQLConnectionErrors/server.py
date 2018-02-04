from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'friendsdb')

### Display records

#@app.route('/')
#def index():
#    return render_template('index.html')

#@app.route('/')
#def index():
#    friends = mysql.query_db("SELECT * FROM friends")
#    print friends
#    return render_template('index.html')


@app.route('/')
def index():
    print 'index'
    query = "SELECT * FROM friends"                           # define your query
    friends = mysql.query_db(query)                           # run query with query_db()
    return render_template('index.html', all_friends=friends) # pass data to our template

### Insert records

@app.route('/friends/<friend_id>')
def show(friend_id):
    print 'show'
    # Write query to select specific user by id. At every point where
    # we want to insert data, we write ":" and variable name.
    query = "SELECT * FROM friends WHERE id = :specific_id"
    # Then define a dictionary with key that matches :variable_name in query.
    ####print query
    data = {'specific_id': friend_id}
    ####print data
    # Run query with inserted data.
    friends = mysql.query_db(query, data)
    print friends
    # Friends should be a list with a single object,
    # so we pass the value at [0] to our template under alias one_friend.
    return render_template('index.html', all_friends=friends)

#@app.route('/friends', methods=['POST'])
#def create():
#    # add a friend to the database!
#    return redirect('/')

#@app.route('/friends', methods=['POST'])
#def create():
#    print request.form['first_name']
#    print request.form['last_name']
#    print request.form['occupation']
#    # add a friend to the database!
#    return redirect('/')

@app.route('/friends', methods=['POST'])
def create():
    print 'create'
    # Write query as a string. Notice how we have multiple values
    # we want to insert into our query.
    query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (:first_name, :last_name, :occupation, NOW(), NOW())"
    # We'll then create a dictionary of data from the POST data received.
    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'occupation': request.form['occupation']
           }
    # Run query, with dictionary values injected into the query.
    mysql.query_db(query, data)
    return redirect('/')


### Update record
@app.route('/update', methods=['POST'])
def update():
    print 'update'
    query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, occupation = :occupation , updated_at = now() WHERE id = :id"
    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'occupation': request.form['occupation'],
             'id': request.form['id']
           }
    mysql.query_db(query, data)
    return redirect('/')

### Delete record

@app.route('/delete/<friend_id>')
def delete(friend_id):
    print 'delete'
    query = "DELETE FROM friends WHERE id = :id"
    data = {'id': friend_id}
    mysql.query_db(query, data)
    return redirect('/')

app.run(debug=True)
