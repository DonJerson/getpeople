from django.shortcuts import render, get_object_or_404
from .models import *
# Create your views here.

def jobs(request):
	block = {'candidates':Candidate.objects.all(), 'positions':Position.objects.all()}
	return render(request, 'jobs.html', block)

def job_view(request, pk):
	instance = get_object_or_404(Position, id=pk)
	block = {
	'positions':Position.objects.all(),
	'instance':instance,
	'candidates':instance.candidate_set.all()
	}
	return render(request, 'job_view.html', block)
    
def candidates_view(request, position_id):
	instance = get_object_or_404(Position, id=position_id)
	candidates=instance.candidate_set.order_by('priority')
	
	block = {

	'positions':Position.objects.all(),
	'candidates':candidates,
	'position':instance
	}
	return render(request, 'candidates_view.html', block)    

def in_call(request, position_id, candidate_id):
	position = Position.objects.get(id=position_id)
	candidate = Candidate.objects.get(id=candidate_id)
	logtemplates = LogTemplate.objects.all()
	context = {
	'positions':Position.objects.all(),
	'candidate': candidate,
	'position':position,
	'logtemplates':logtemplates
	}
	return render(request, 'in_call.html', context)
	
def disposition(request, position_id, candidate_id, logtemplate_id):
	recruiter = request.user.recruiter
	candidate = Candidate.objects.get(id=candidate_id)
	log_template = LogTemplate.objects.get(id=logtemplate_id)
	new_log = Log(action=log_template.action, recruiter=recruiter, candidate=candidate)
	new_log.save()
	candidate.priority = candidate.priority - log_template.priority_offset
	other_object = candidate.log_set.add(new_log)
	
	instance = get_object_or_404(Position, id=position_id)
	candidates=instance.candidate_set.all()
	block = {
	'positions':Position.objects.all(),
	'candidates':candidates,
	'position':instance
	}
	
	return render(request, 'candidates_view.html', block)
	
	
def login_view(request):
	title = "Login"
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
	return render(request, "form.html", {'form':form,'title':title})
