from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.encoding import python_2_unicode_compatible
from tinymce import models as tinymce_models
# Create your models here.

class Position(models.Model):
	name = models.CharField(max_length=200)
	salary_anual = models.IntegerField()
	description = models.TextField()
	skills = models.TextField()
	location = models.CharField(max_length=200)

	# status_choices = (
		# (y, 'Active'),
		# (n, 'Closed')
	# )
	# status = models.CharField(
		# max_length=1,
		# choices=status_choices,
		# default=y,
	# )
	def __unicode__(self):
		return u'%s' % self.name
	pass
	
	def get_absolute_url(self):
		return reverse("job_view", kwargs={"id":self.id})
	@property
	def show_candidates(self):
		return [self.candidate_set.all()]


class Candidate(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField(max_length=150, null=False, unique=True)
	phone = models.CharField(max_length=20, null=False, unique=True, default=uuid.uuid1)
	resume = models.FileField(upload_to="static/media")
	position = models.ForeignKey(Position)
	priority = models.IntegerField(default=0)
	pass
	
	@property
	def logs(self):
		return self.log_set.all().order_by('-created')
	
	def __unicode__(self):
		return unicode(self.name)
		
	def get_absolute_url(self):
		return reverse("candidate_view", kwargs={"id":self.id})
		


class Recruiter(models.Model):
	name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField()
	picture = models.FileField(null=True)
	user = models.OneToOneField(User)
	pass
	
	def __unicode__(self):
		return self.name

class LogTemplate(models.Model):
	action = models.CharField(max_length=100)
	priority_offset = models.IntegerField()
	def __unicode__(self):
		return self.action
	pass

class Log(models.Model):
	action = models.CharField(max_length=100)
	recruiter = models.ForeignKey(Recruiter)
	candidate = models.ForeignKey(Candidate)
	note = models.CharField(max_length=300, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.action
