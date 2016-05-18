from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import *
from django.core.urlresolvers import reverse
from .forms import *
# Create your views here.

def jobs(request):
	if request.user.is_authenticated():
		recruiter = request.user.recruiter
	else: recruiter = 0

	block = {
	'recruiter':recruiter,

	'candidates':Candidate.objects.all(),
	'positions':Position.objects.all()}
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
	candidate.priority = candidate.priority + log_template.priority_offset
	other_object = candidate.log_set.add(new_log)
	
	instance = get_object_or_404(Position, id=position_id)
	candidates=instance.candidate_set.all()

	url = reverse('candidates_view', kwargs={
	'position_id':position_id})
	return HttpResponseRedirect(url)

def add_candidate(request):
	form = CandidateForm(request.POST, request.FILES)
	context = {
	'form':form
	}
	if request.method == 'POST':	
		form = CandidateForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('jobs'))
	return render(request, 'add_candidate.html', context)
	

def login_function(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('jobs'))
                
def logout_function(request):
	logout(request)
	return HttpResponseRedirect(reverse('jobs'))
	
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username,password=password)
    return HttpResponseRedirect(reverse('jobs'))
