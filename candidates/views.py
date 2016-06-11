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
	'positions':Position.objects.all().order_by('name')}
	return render(request, 'jobs.html', block)

def job_view(request, pk):
	instance = get_object_or_404(Position, id=pk)
	block = {
	'positions':Position.objects.all().order_by('name'),
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
	string_salary = str(position.salary_anual)
	position.salary_anual = "USD $"+string_salary
	candidate = Candidate.objects.get(id=candidate_id)
	logtemplates = LogTemplate.objects.all()
	form = NoteForm(request.POST)
	
	context = {
	'positions':Position.objects.all(),
	'candidate': candidate,
	'position':position,
	'logtemplates':logtemplates,
	'form':form
	}
	return render(request, 'in_call.html', context)
	
def disposition(request, position_id, candidate_id):
	recruiter = request.user.recruiter
	candidate = Candidate.objects.get(id=candidate_id)
	log_template = LogTemplate.objects.all()
	for log_type in log_template:
		if log_type.action in request.POST:
			log = log_type
			break
	
	new_log = Log(action=log.action, recruiter=recruiter, candidate=candidate)
	new_log.save()
	candidate.priority = candidate.priority + log.priority_offset
	other_object = candidate.log_set.add(new_log)
	candidate.save()

	f = NoteForm(request.POST, instance=new_log)
	f.save()
	
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
		if form.is_valid():
			instance = form.save(commit=False)
			if "save" in request.POST:
				instance.save()
				return HttpResponseRedirect(reverse('add_candidate'))
			elif "call_candidate" in request.POST:
		
				instance.save()
				candidate_id = instance.id
				position_id = instance.position.id
				
				url = reverse('in_call', kwargs={
				'position_id':position_id, 'candidate_id':candidate_id})
				return HttpResponseRedirect(url)
	return render(request, 'add_candidate.html', context)

	

def login_function(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('jobs'))
                
def logout_function(request):
	logout(request)
	return HttpResponseRedirect(reverse('jobs'))
	
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username,password=password)
    return HttpResponseRedirect(reverse('jobs'))


