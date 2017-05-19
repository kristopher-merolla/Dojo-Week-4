# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse

import datetime, calendar

# Create your views here.

def index(request):
	month = calendar.month_name[int(str(datetime.datetime.now()).split(" ")[0].split("-")[1])]
	day = str(datetime.datetime.now()).split(" ")[0].split("-")[2]
	year = str(datetime.datetime.now()).split(" ")[0].split("-")[0]

	date = month+" "+day+", "+year
	time = datetime.datetime.time(datetime.datetime.now())

	context = {
	"date":date,
	"time": time
	}

	return render(request, 'time_display/index.html', context)