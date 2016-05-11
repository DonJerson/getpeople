from django.shortcuts import render, get_object_or_404
from .models import Candidate
from .models import Position
# Create your views here.
def jobs(request):
	block = {'candidates':Candidate.objects.all(), 'positions':Position.objects.all()}
	return render(request, 'jobs.html', block)

def job_view(request, pk):
	instance = get_object_or_404(Position, id=pk)
	block = {
	'instance':instance,
	'candidates':instance.candidate_set.all()
	}
	return render(request, 'job_view.html', block)
    
def candidates_view(request, id):
	instance = get_object_or_404(Position, id=id)
	candidates=instance.candidate_set.all()
	block = {
	'candidates':candidates,
	'positions':instance
	}
	return render(request, 'candidates_view.html', block)    
