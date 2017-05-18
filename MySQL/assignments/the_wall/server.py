from flask import Flask, request, redirect, render_template, session, flash

from mysqlconnection import MySQLConnector # needed to connect to SQL

from validate_email import validate_email # import to check if email submitted is valid!

import md5 # imports the md5 module to generate a hash for password securing

import os, binascii # used for random generation // salt = binascii.b2a_hex(os.urandom(15))

app = Flask(__name__)

mysql = MySQLConnector(app,'thewalldb') #database name goes here!

app.secret_key = 's3cr3tk3y' # set secret key for session data

@app.route('/') # login/register page
def index():
	if (session.get('active_user') == None):
		return render_template('index.html')
	else:
		session['active_user'] = None
		return render_template('index.html')

@app.route('/register') # register new user
def register():
	return render_template('register.html')

@app.route('/thewall') # redirect to here when login successful
def active_user():
	if (session.get('active_user') == None): # if no active user, redirect to the login page
		return redirect('/')
	else:
		query_posts = "SELECT posts.id,CONCAT(users.first_name,' ',users.last_name) AS name,posts.message,CONCAT(MONTHNAME(posts.created_at), ' ', DAY(posts.created_at), ', ', YEAR(posts.created_at)) AS date from posts join users on users.id = posts.user_id"
		posts = mysql.query_db(query_posts)
		return render_template('active.html', all_posts = posts) # if active user is available, go to the wall (active.html)

# PAGE TO LOGIN EXISTING USER
@app.route('/login', methods=['POST'])
def login():
	email = request.form['email']
	password = request.form['password'] # password needs to be hashed here, use md5 and a salt

	# validate login credentials here
	email_exists = "SELECT COUNT(*) FROM users WHERE email = :email"
	exists_data = {'email': email}
	if (mysql.query_db(email_exists,exists_data)[0]['COUNT(*)'] == 1): # email is in the database
		# grab salt from the database and use it to rehash our submitted login password
		grab_salt = "SELECT salt FROM users WHERE email = :email"
		salt_data = {'email': email}
		salt = mysql.query_db(grab_salt,salt_data)
		login_password = md5.new(password + salt[0]['salt']).hexdigest() # the password entered at login screen, hashed with salt
		# grab the registered hashed password from db
		grab_hash = "SELECT password FROM users WHERE email = :email"
		hash_data = {'email': email}
		hashed_pw = mysql.query_db(grab_hash,hash_data) # the hashed password stored in the data for the given email
		if (login_password == hashed_pw[0]['password']):
			#passwords match, login
			session['active_user'] = email
			return redirect('/thewall')
		else:
			# display error message password invalid (does not match database entry)
			error_message = "<p style='color:red;'> INVALID PASSWORD </p> "
			return render_template('index.html',error_message=error_message)
	else:
		# display error message email does not exist in database
		error_message = "<p style='color:red;'> EMAIL NOT REGISTERED </p> "
		return render_template('index.html',error_message=error_message)

# PAGE TO REGISTER NEW USER
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

	# Frist and last name need to be at least 2 characters, otherwise error
	if (len(first_name) < 2 or len(last_name) < 2):
		error_message = "<p style='color:red;'> NAME FIELDS MUST BE AT LEAST 2 CHARACTERS </p> "
		return render_template('register.html',error_message=error_message)
	# Frist and last name need to be only alpha (no numbers or special characters)
	if (not(first_name.isalpha()) or not(first_name.isalpha())):
		error_message = "<p style='color:red;'> NAME FIELDS CANT CONTAIN NUMBERS OR SPECIAL CHARACTERS </p> "
		return render_template('register.html',error_message=error_message)
	
	# before inserting the user, validate email and password
	email_exists = "SELECT COUNT(*) FROM users WHERE email = :email"
	exists_data = {'email': email}
	if (mysql.query_db(email_exists,exists_data)[0]['COUNT(*)'] == 0): # if the email is NOT in the database...
		if (validate_email(request.form['email'])): # if the email IS valid...
			if (password == password_confirm): # if the password matches the confirmation password
				if (len(password) >= 8): # if the length of the password is 8 characters or more
					#build and execute the SQL insert for a new user creation
					query_data = { 'first_name': first_name, 'last_name': last_name, 'email': email, 'hashed_pw': hashed_pw, 'salt': salt}
					insert_query = "INSERT INTO users (first_name, last_name, email, password, salt, created_at, updated_at) VALUES (:first_name, :last_name, :email, :hashed_pw, :salt, NOW(), NOW())"
					mysql.query_db(insert_query, query_data)
					# if all validations are met and the data is updated, redirect to the home page for login
					return redirect('/')
				else:
					# display error message password too short
					error_message = "<p style='color:red;'> PASSWORD TOO SHORT </p> "
					return render_template('register.html',error_message=error_message)
			else:
				# display error message password not matching password confirmation
				error_message = "<p style='color:red;'> PASSWORDS DO NOT MATCH </p> "
				return render_template('register.html',error_message=error_message)
		else:
			# display error message if email is not a valid email
			error_message = "<p style='color:red;'> INVALID EMAIL </p> "
			return render_template('register.html',error_message=error_message)
	else:
		# display error message if email already exists
		error_message = "<p style='color:red;'> EMAIL ALREADY EXISTS </p> "
		return render_template('register.html',error_message=error_message)


@app.route('/post', methods=['POST'])
def new_post():
	if (session.get('active_user') == None): # if no active user, redirect to the login page
		return redirect('/')
	# if we are dealing with a new post (NOT a new comment)
	if (request.form['new_post'] == 'new_post'):
		# set message to our form submission
		message = request.form['post']
		# check if the post was sent in blank
		if (message == ""):
			return	redirect('/thewall')
		else:
			# grab the user_id for the active user from the users table
			grab_user_id = "SELECT id FROM users WHERE email = :email"
			grab_data = {'email': session['active_user']}
			user_id = mysql.query_db(grab_user_id, grab_data)[0]['id']
			# add the new post into the posts table
			new_post = "INSERT INTO posts (user_id, message, created_at, updated_at) VALUES (:user_id, :message, NOW(), NOW())"
			post_data = {'user_id': user_id, 'message': message}
			mysql.query_db(new_post, post_data)
			return redirect('/thewall')
	# if we are dealing with a new comment (NOT a new post)
	if (request.form['new_post'] == 'new_comment'):
		print "new comment"
		return	redirect('/thewall/comment')


@app.route('/thewall/comment') # redirect to here when login successful
def active_comment():
	if (session.get('active_user') == None): # if no active user, redirect to the login page
		return redirect('/')
	else:
		query_posts = "SELECT posts.id,CONCAT(users.first_name,' ',users.last_name) AS name,posts.message,CONCAT(MONTHNAME(posts.created_at), ' ', DAY(posts.created_at), ', ', YEAR(posts.created_at)) AS date from posts join users on users.id = posts.user_id"
		posts = mysql.query_db(query_posts)
		return render_template('active.html', all_posts = posts) # if active user is available, go to the wall (active.html)


app.run(debug=True)




