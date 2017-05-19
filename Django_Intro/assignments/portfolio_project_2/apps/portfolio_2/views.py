# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.

def index(request):
	return render(request, 'portfolio_2/index.html')

def projects(request):
	return render(request, 'portfolio_2/projects.html')

def about_me(request):
	return render(request, 'portfolio_2/about_me.html')

def testimonials(request):
	return render(request, 'portfolio_2/testimonials.html')