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

def update(request):
	def rem_spaces(string):
		counter = 0
		for char in string:
			if char != ' ':
				new_string = string[counter:]
				break
			else: counter += 1
		return new_string

	def clean_spaces(string):
		x = rem_spaces(string)
		final = rem_spaces(x[::-1])
		return final[::-1]

	candidates = Candidate.objects.all()
	for candidate in candidates:
		candidate.name = clean_spaces(candidate.name).title()
		candidate.email = candidate.email.lower()
		candidate.save()
	url = reverse('jobs')
	return HttpResponseRedirect(url)
	
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

def send_email(request, candidate_id):
	recruiter = request.user.recruiter
	candidate = Candidate.objects.get(id=candidate_id)
	position_id = candidate.position.id
	position = candidate.position
	
	import smtplib
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	import os
	import webbrowser


	FROM = recruiter.email
	TO = [candidate.email, recruiter.email] # must be a list

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Job opportunity!"
	msg['From'] = recruiter.email
	msg['To'] = candidate.email


	description = """<pre>%s</pre>""" % (position.description)
	skills = """<pre>%s</pre>""" % (position.skills)

	intro = """My name is %s %s, I am a Staff Recruiter specialist from Barrister. We are a nation-wide agency filling full time job positions for some of the largest corporations in the US. I found your resume online and I believe you are a good candidate for a job opening we have. Down bellow you will find the job description, please reply back to this email if you are interested in this opportunity.""" % (recruiter.name, recruiter.last_name)
	signature = """
<pre>
%s
Staff Recruiter Administrator
Manager: Cesar de la Cruz
Barrister Global Services Network, Inc.
PO Box 1979
Hammond, LA 70404-1979
Manager: Cesar De La Cruz
Phone:	985-365-0400 ext 471
Fax:	985-310-5530
E-mail:	%s

URL:	www.barrister.com

-------------------------------------------
COMPANY CONFIDENTIAL: This email and any files transmitted with it are confidential and intended solely for the use of the individual or entity to whom they are addressed. If the reader of this message is not the intended recipient(s), you are notified that you have received this message in error and that any review, dissemination, distribution or copying of this message is strictly prohibited. If you have received this message in error, please delete this message and notify the sender immediately. Please note that any views or opinions presented in this email are solely those of the author and do not necessarily represent those of the company.
WARNING: Computer viruses can be transmitted via email. The recipient should check this email and any attachments for the presence of viruses. The company accepts no liability for any damage caused by any virus transmitted by this email.
Opinions, conclusions and other information in this message that do not relate to the official business of Barrister Global Services Network, Inc. or its subsidiaries shall be understood as neither given nor endorsed by it.
-------------------------------------------
</pre>
	""" % (recruiter.name, recruiter.email)

	text = "Please use a mail system that supports html format"
	html = """
	<html>
	  <head>
		<style type="text/css" style="display: none">
		#subheaders {
		  font-weight: bold;
		  display: inline;
		}
		.p {
		  display: inline;
		}
		</style>
	  </head>
	  <body>
		<p>Hello %s,</p>
		<p>%s</p><br>
		<h3>%s</h3>
		<h4 id='subheaders'>Job location: %s</h4>
		<h4 id='subheaders'>Annual Salary: USD $%s</h4><br>
		<h4>Job Description:</h4>
		<p>%s</p><br>
		<h4>Required skills and additional information:</h4>
		<p>%s</p><br><br>
		<p>Sincerely,</p><br><br>
	<p>%s</p><br>
		
		
	  </body>
	</html>
	""" % (candidate.name, intro, position.name, position.location, position.salary_anual, description, skills, signature)
	
	html = u'%s' % html

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)

	# Send the mail

	barrister = 'mail.barrister.com'

	server = smtplib.SMTP(barrister)
	server.ehlo()
	server.starttls()
	server.ehlo
	server.login(recruiter.email, 'Barrister123')
	server.sendmail(FROM, TO, msg.as_string())
	server.close()
	
	new_log = Log(action='Emailed', recruiter=recruiter, candidate=candidate)
	new_log.save()
	
	url = reverse('candidates_view', kwargs={
	'position_id':position_id})
	return HttpResponseRedirect(url)
