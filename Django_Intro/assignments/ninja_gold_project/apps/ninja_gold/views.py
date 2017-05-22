# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

import random # import the random module

# Create your views here.
def index(request):
	return render(request, 'ninja_gold/index.html')

def process_money(request):

	if (request.method=="POST"):
		print "request to process_money"
		request.session['building'] = request.POST['building']
	else:
		redirect('/')

	if (request.session.get('activity') == None):
		request.session['activity'] = "Welcome New Player"
		request.session['gold_amt'] = 0

	if (request.session['building'] == 'farm'):
		print "FARM ROLL"
		roll = random.randrange(10, 20)
		request.session['gold_amt'] += roll
		request.session['activity'] += "<p style='color: green;'> Earned "+str(roll)+" gold from the farm! </p>"

	if (request.session['building'] == 'cave'):
		print "CAVE ROLL"
		roll = random.randrange(5, 10)
		request.session['gold_amt'] += roll
		request.session['activity'] += "<p style='color: green;'> Earned "+str(roll)+" gold from the cave! </p>"

	if (request.session['building'] == 'house'):
		print "HOUSE ROLL"
		roll = random.randrange(2, 5)
		request.session['gold_amt'] += roll
		request.session['activity'] += "<p style='color: green;'> Earned "+str(roll)+" gold from the house! </p>"

	if (request.session['building'] == 'casino'):
		print "CASINO ROLL"
		roll = random.randrange(-50, 50)
		request.session['gold_amt'] += roll
		if (roll >= 0):
			request.session['activity'] += "<p style='color: green;'> Earned "+str(roll)+" gold from the casino! You're lucky!</p>"
		if (roll < 0):
			roll *= -1
			request.session['activity'] += "<p style='color: red;'> Lost "+str(roll)+" gold from the casnio! Better luck next time...</p>"

	print request.session['activity']

	return redirect('/')