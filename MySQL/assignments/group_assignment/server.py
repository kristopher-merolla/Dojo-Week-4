from flask import Flask, request, redirect, render_template, session, flash

from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql = MySQLConnector(app,'groupassignmentdb')

@app.route('/')
def index():
	query = "SELECT * FROM users"                           # define your query
	users = mysql.query_db(query)                         # run query with query_db()
	return render_template('index.html', all_users=users) # pass data to our template

@app.route('/users/create', methods=['POST'])
def create():
	# Write query as a string. Notice how we have multiple values
	# we want to insert into our query.
	query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW())"
	# We'll then create a dictionary of data from the POST data received.
	data = {
			'first_name': request.form['first_name'],
			'last_name':  request.form['last_name'],
			'email': request.form['email']
			}
	# Run query, with dictionary values injected into the query.
	mysql.query_db(query, data)
	return redirect('/')

@app.route('/users/update', methods=['POST'])
def update():
	# Write query as a string. Notice how we have multiple values
	# we want to insert into our query.
	query = "UPDATE users set first_name = :first_name, last_name = :last_name, email = :email, updated_at = NOW() where id = :user_id"
	# We'll then create a dictionary of data from the POST data received.
	data = {
			'first_name': request.form['first_name'],
			'last_name':  request.form['last_name'],
			'email': request.form['email'],
			'user_id': request.form['user_id']
			}
	# Run query, with dictionary values injected into the query.
	mysql.query_db(query, data)
	return redirect('/users/'+request.form['user_id'])

@app.route('/users/<user_id>')
def show(user_id):
	query = "SELECT * FROM users where id = :user_id"                      # define your query
	data = {'user_id': user_id}
	user = mysql.query_db(query,data)                           # run query with query_db()
	return render_template('user.html', user=user[0]) # pass data to our template

@app.route('/users/new')
def new():

	return render_template('new.html') # pass data to our template

@app.route('/users/<user_id>/edit')
def edit(user_id):
	query = "SELECT * FROM users where id = :user_id"                      # define your query
	data = {'user_id': user_id}
	user = mysql.query_db(query,data)                           # run query with query_db()
	return render_template('edit.html', user=user[0]['id']) # pass data to our template

@app.route('/users/<user_id>/delete')
def delete(user_id):
	print user_id
	query = "DELETE FROM users where id = :user_id"
	data = {'user_id': user_id}
	mysql.query_db(query, data)
	return redirect('/')

app.run(debug=True)




