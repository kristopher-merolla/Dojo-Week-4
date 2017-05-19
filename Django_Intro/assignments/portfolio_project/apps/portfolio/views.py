# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.

def index(request):
	return render(request, 'portfolio/index.html')

def testimonials(request):
	return render(request, 'portfolio/testimonials.html')