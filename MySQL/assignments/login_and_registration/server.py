from flask import Flask, request, redirect, render_template, session, flash

from mysqlconnection import MySQLConnector

from validate_email import validate_email # import to check if email submitted is valid!

app = Flask(__name__)
mysql = MySQLConnector(app,'loginandregisterdb') #database name goes here!

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
	email = request.form['email']
	password = request.form['password'] #password needs to be hashed here, use md5 and a salt

	#validate login credentials here
	return redirect('/') #if invalid login credentials
	return render_template('active.html') #if valid login credentials


@app.route('/register')
def register():
	return render_template('register.html')


@app.route('/register_user', methods=['POST'])
def new_login():
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	email = request.form['email']
	password = request.form['password'] #password needs to be hashed here, use md5 and a salt

	#validate registration credentials here
	return redirect('/') #if invalid registration credentials send back to login screen
	return render_template('active.html') #if valid register credentials go to active page



app.run(debug=True)




