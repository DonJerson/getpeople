from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$', views.jobs, name='jobs'),
	url(r'^login/$', views.login_function, name='login'),
	url(r'^logout/$', views.logout_function, name='logout'),
	url(r'^add_candidate/$', views.add_candidate, name='add_candidate'),
	url(r'^jobs/(?P<position_id>\d+)/$', views.candidates_view, name='candidates_view'),
	url(r'^jobs/(?P<position_id>\d+)/(?P<candidate_id>\d+)/in_call/$', views.in_call, name='in_call'),
	url(r'^jobs/(?P<position_id>\d+)/(?P<candidate_id>\d+)/(?P<logtemplate_id>\d+)/disposition/$', views.disposition , name='disposition'),
]
