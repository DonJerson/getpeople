from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$', views.login_view, name='login'),
	url(r'^jobs/$', views.jobs, name='jobs'),
	url(r'^jobs/(?P<position_id>\d+)/$', views.candidates_view, name='candidates_view'),
	url(r'^jobs/(?P<position_id>\d+)/(?P<candidate_id>\d+)/in_call/$', views.in_call, name='in_call'),
	url(r'^jobs/(?P<position_id>\d+)/(?P<candidate_id>\d+)/(?P<logtemplate_id>\d+)/disposition/$', views.disposition , name='disposition'),
]
