# add some routes for application urls.py #if you dont do this first you will get a circular import error
from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index),
  url(r'^testimonials', views.testimonials),
]