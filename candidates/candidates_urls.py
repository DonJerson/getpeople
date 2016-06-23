from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$', views.jobs, name='jobs'),
	url(r'^login/$', views.login_function, name='login'),
	url(r'^update/$', views.update, name='update'),
	url(r'^search/$', views.search, name='search'),
	url(r'^logout/$', views.logout_function, name='logout'),
	url(r'^delete_candidate/(?P<candidate_id>\d+)/$', views.delete_candidate, name='delete_candidate'),
	url(r'^add_candidate/$', views.add_candidate, name='add_candidate'),
	url(r'^jobs/(?P<position_id>\d+)/$', views.candidates_view, name='candidates_view'),
	url(r'^jobs/(?P<position_id>\d+)/(?P<candidate_id>\d+)/in_call/$', views.in_call, name='in_call'),
	url(r'^jobs/(?P<position_id>\d+)/(?P<candidate_id>\d+)/disposition/$', views.disposition , name='disposition'),
	url(r'^single_candidate/(?P<candidate_id>\d+)/$', views.single_candidate , name='single_candidate'),
	url(r'^send_email/(?P<candidate_id>\d+)/$', views.send_email, name='send_email'),
]
