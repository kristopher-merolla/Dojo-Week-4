from flask import Flask, request, redirect, render_template, session, flash

from mysqlconnection import MySQLConnector

from validate_email import validate_email # import to check if email submitted is valid!

app = Flask(__name__)
mysql = MySQLConnector(app,'loginandregisterdb') #database name goes here!

@app.route('/')
def index():
	return render_template('index.html')







app.run(debug=True)




