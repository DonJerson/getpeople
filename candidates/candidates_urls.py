from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$', views.jobs, name='jobs'),
	url(r'^(?P<id>\d+)/$', views.candidates_view, name='candidates_view')
]
