from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$', views.jobs, name='jobs'),
	url(r'^1099/$', views.jobs_1099, name='jobs_1099'),
	url(r'^login/$', views.login_function, name='login'),
	url(r'^update/$', views.update, name='update'),
	url(r'^search/$', views.search, name='search'),
	url(r'^logout/$', views.logout_function, name='logout'),
	url(r'^delete_candidate/(?P<candidate_id>\d+)/$', views.delete_candidate, name='delete_candidate'),
	url(r'^rec_profile/(?P<days>\d+)/$', views.rec_profile, name='rec_profile'),
	url(r'^main_wall/(?P<days>\d+)/$', views.main_wall, name='main_wall'),
	url(r'^add_candidate/$', views.add_candidate, name='add_candidate'),
	url(r'^jobs/(?P<position_id>\d+)/$', views.candidates_view, name='candidates_view'),
	url(r'^in_call/(?P<candidate_id>\d+)/$', views.in_call, name='in_call'),
	url(r'^disposition/(?P<candidate_id>\d+)/$', views.disposition , name='disposition'),
	url(r'^single_candidate/(?P<candidate_id>\d+)/$', views.single_candidate , name='single_candidate'),
	url(r'^send_email/(?P<candidate_id>\d+)/$', views.send_email, name='send_email'),
]
