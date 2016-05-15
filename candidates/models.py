from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Position(models.Model):
	name = models.CharField(max_length=200)
	salary_anual = models.IntegerField()
	description = models.TextField()
	skills = models.TextField()
	location = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.name
	pass
	
	def get_absolute_url(self):
		return reverse("job_view", kwargs={"id":self.id})
	@property
	def show_candidates(self):
		return [self.candidate_set.all()]


class Candidate(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField(max_length=150)
	phone = models.CharField(max_length=20)
	resume = models.TextField()
	position = models.ForeignKey(Position)
	priority = models.IntegerField(default=0)
	pass
	
	def __unicode__(self):
		return self.name
		
	def get_absolute_url(self):
		return reverse("candidate_view", kwargs={"id":self.id})
		


class Recruiter(models.Model):
	name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField()
	user = models.OneToOneField(User)
	pass
	
	def __unicode__(self):
		return self.name

class LogTemplate(models.Model):
	action = models.CharField(max_length=100)
	priority_offset = models.IntegerField()
	pass

class Log(models.Model):
	action = models.CharField(max_length=100)
	recruiter = models.ForeignKey(Recruiter)
	candidate = models.ForeignKey(Candidate)
	created = models.DateTimeField(auto_now_add=True)
