from django.db import models

# Create your models here.

class Position(models.Model):
	name = models.CharField(max_length=200)
	salary = models.IntegerField()
	description = models.TextField()
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
    
	def __unicode__(self):
		return self.name
		
	def get_absolute_url(self):
		return reverse("candidate_view", kwargs={"id":self.id})
