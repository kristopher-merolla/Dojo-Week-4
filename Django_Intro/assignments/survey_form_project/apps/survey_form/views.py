# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.

def index(request):
	return render(request, 'survey_form/index.html')

def submit_survey(request):
	if (request.method=="POST"):
		# print request.method
		# print request.POST['name']
		request.session['name'] = request.POST['name']
		request.session['location'] = request.POST['location']
		request.session['language'] = request.POST['language']
		request.session['comment'] = request.POST['comment']
		return redirect('/submitted')
	else:
		return redirect('/')

def submitted(request):
	return render(request, 'survey_form/success.html')