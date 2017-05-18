from flask import Flask, request, redirect, render_template, session, flash

from mysqlconnection import MySQLConnector # needed to connect to SQL

from validate_email import validate_email # import to check if email submitted is valid!

import md5 # imports the md5 module to generate a hash for password securing

import os, binascii # used for random generation // salt = binascii.b2a_hex(os.urandom(15))

from validate_email import validate_email # import to check if email submitted is valid!

app = Flask(__name__)
mysql = MySQLConnector(app,'loginandregisterdb') #database name goes here!

@app.route('/') # login/register page
def index():
	return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
	email = request.form['email']
	password = request.form['password'] # password needs to be hashed here, use md5 and a salt

	# validate login credentials here

	# if invalid login credentials
	return redirect('/')

	# if valid login credentials
	return render_template('active.html')


@app.route('/register')
def register():
	return render_template('register.html')


@app.route('/register_user', methods=['POST'])
def new_login():
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	email = request.form['email']
	#password needs to be hashed here, use md5 and a salt
	password = request.form['password']
	password_confirm = request.form['password_confirmation']
	salt =  binascii.b2a_hex(os.urandom(15)) # salt is stored in the database for validation
	hashed_pw = md5.new(password + salt).hexdigest() # this is stored in the database as the password, now secure
	
	#before inserting the user, validate entry
	email_exists = "SELECT COUNT(*) FROM users WHERE email = :email"
	exists_data = {'email': email}
	if (mysql.query_db(email_exists,exists_data)[0]['COUNT(*)'] == 0): # if the email is NOT in the database...
		if (validate_email(request.form['email'])):
			if (password == password_confirm):
				#build and execute the SQL insert for a new user creation
				query_data = { 'first_name': first_name, 'last_name': last_name, 'email': email, 'hashed_pw': hashed_pw, 'salt': salt}
				insert_query = "INSERT INTO users (first_name, last_name, email, password, salt, created_at, updated_at) VALUES (:first_name, :last_name, :email, :hashed_pw, :salt, NOW(), NOW())"
				mysql.query_db(insert_query, query_data)
			else:
				# display error message password not matching password confirmation
				print "ERROR< PASSWORDS DO NOT MATCH"
				return redirect('/register')			
		else:
			# display error message if email is not a valid email
			print "ERROR< EMAIL INVALID"
			return redirect('/register')
	else:
		# display error message if email already exists
		print "ERROR EMAIL EXISTS"
		return redirect('/register')

	# if all validations are met and the data is updated, redirect to the home page for login
	return redirect('/')


app.run(debug=True)




