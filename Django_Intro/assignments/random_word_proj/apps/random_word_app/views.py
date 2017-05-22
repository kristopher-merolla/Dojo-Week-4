# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

import string, random
	


# Create your views here.
def index(request):

	return render(request, 'random_word_app/index.html')

def generate(request):

	request.session['random_word'] = ""

	if request.method == "POST":
		for i in range (14):
			request.session['random_word'] += random.choice(string.letters)
		return redirect("/")
	else:
		return redirect("/")