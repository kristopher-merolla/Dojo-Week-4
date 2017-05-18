from flask import Flask, request, redirect, render_template, session, flash

from mysqlconnection import MySQLConnector

from validate_email import validate_email # import to check if email submitted is valid!

app = Flask(__name__)
mysql = MySQLConnector(app,'emailvalidationdb') #database name goes here!

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
	# validate email input before saving into database
	if (validate_email(request.form['email'])):
		query = "INSERT INTO users (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
		# We'll then create a dictionary of data from the POST data received.
		data = {
				'email': request.form['email']
				}
		# Run query, with dictionary values injected into the query.
		mysql.query_db(query, data)
		query2 = "SELECT * FROM users"
		emails = mysql.query_db(query2)
		return render_template('success.html', all_emails = emails, email_added = request.form['email'])
	else:
		print "invalid email"
		return redirect('/invalid')


@app.route('/invalid')
def invalid():
	return render_template('invalid.html')





app.run(debug=True)




