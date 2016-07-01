from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import *
from django.core.urlresolvers import reverse
from .forms import *
from django.core.mail import send_mail
from datetime import datetime, timedelta
# Create your views here.

def rec_profile(request, days):
	rec = request.user.recruiter
	all_logs = rec.log_set.filter(created__gte=datetime.now()-timedelta(days=int(days)))
	logs_number = len(all_logs)
	block = {
	'recruiter':rec,
	'logs':all_logs,
	'days':days,
	'logs_number':logs_number
	}
	return render(request, 'rec_profile.html', block)
	
def main_wall(request, days):

	recs = Recruiter.objects.all()
	#all_logs = rec.log_set.all()
	updated_recs = list()
	total = 0
	for rec in recs:
		rec.logs_number = len(rec.log_set.filter(created__gte=datetime.now()-timedelta(days=int(days))))
		if rec.logs_number != 0:
			updated_recs.append(rec)

	block = {
	'recruiters':updated_recs
	#'logs':all_logs
	}
	return render(request, 'main_wall.html', block)
	
def delete_candidate(request, candidate_id):
	candidate = Candidate.objects.get(id=candidate_id)
	candidate.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def jobs_1099(request):
	if request.user.is_authenticated():
		recruiter = request.user.recruiter
	else: recruiter = 0
	
	positions = list()
	for position in Position.objects.all().order_by('name'):
		if '1099' in position.name:
			positions.append(position)
	block = {
	'recruiter':recruiter,
	'candidates':Candidate.objects.all(),
	'positions':positions}
	return render(request, 'jobs_1099.html', block)	
	
def jobs(request):
	if request.user.is_authenticated():
		recruiter = request.user.recruiter
	else: recruiter = 0
	
	positions = list()
	for position in Position.objects.all().order_by('name'):
		if '1099' not in position.name:
			positions.append(position)
			
	block = {
	'recruiter':recruiter,
	'candidates':Candidate.objects.all(),
	'positions':positions}
	return render(request, 'jobs.html', block)
	
def search(request):
	def is_number(s):
		try:
			int(s)
			return True
		except ValueError:
			return False

	def clean_number(phone_number):
		cleaned_number = ''
		for char in phone_number:
			if is_number(char):
				cleaned_number += char          
		return cleaned_number

	if request.method == 'POST':
		search = request.POST['search'].lower()
		all_candidates = Candidate.objects.all()
		selected_candidates = list()
		for candidate in all_candidates:
			if ((search in candidate.name.lower()) or (clean_number(search) in clean_number(candidate.phone) and (clean_number(search))) or (search in candidate.email.lower())):
				selected_candidates.append(candidate)
		number=len(selected_candidates)
		return render(request, 'search.html', {'candidates':selected_candidates,'number':number})
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

def in_call(request, candidate_id):
	candidate = Candidate.objects.get(id=candidate_id)
	position_id = candidate.position.id
	position = Position.objects.get(id=position_id)
	
	logtemplates = LogTemplate.objects.all()
	form = NoteForm(request.POST)
	
	context = {
	'positions':Position.objects.all(),
	'candidate': candidate,
	'position':position,
	'logtemplates':logtemplates,
	'form':form
	}
	if '1099' in position.name:
		return render(request, 'in_call_1099.html', context)
	else:
		return render(request, 'in_call.html', context)
	
def disposition(request, candidate_id):
	candidate = Candidate.objects.get(id=candidate_id)
	recruiter = request.user.recruiter
	position_id = candidate.position.id
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
	if '1099' in position.name:
		intro_change = 'contractor employees'
		salary_change = 'Starting pay per work order:'
	else:
		intro_change = 'full time jobs'
		salary_change = 'Annual Salary:'
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

	description = """%s""" % (position.description)
	skills = """%s""" % (position.skills)
	intro = """My name is %s %s, I am a Staff Recruiter specialist from Barrister. We are a nation-wide agency filling in %s for some of the largest corporations in the US. I found your resume online and I believe you are a great candidate for a job opening we have. Down bellow you will find the job description, please reply back to this email if you are interested in this opportunity.""" % (recruiter.name, recruiter.last_name, intro_change)

	signature = """
%s %s
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
-------------------------------------------""" % (recruiter.name, recruiter.last_name, recruiter.email)

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
		.pre {
		  font-size: 16px;
		}
		</style>
	  </head>
	  <body>
		<p style="font-size:16px;font-family:calibri">Hello %s,</p>
		<p style="font-size:16px;font-family:calibri">%s</p><br>
		<h3>%s</h3>
		<h4 id='subheaders'>Job location: %s</h4>
		<h4 id='subheaders'>%s USD $%s</h4><br>
		<h4>Job Description:</h4>
		<pre style="font-size: 16px;font-family:calibri">%s</pre><br>
		<h4>Required skills and additional information:</h4>
		<pre style="font-size: 16px;font-family:calibri">%s</pre><br><br>
		<p style="font-size:16px;font-family:calibri">Sincerely,</p><br><br>
	<pre style="font-size:16px;font-family:calibri">%s<pre><br>
		
		
	  </body>
	</html>
	""" % (candidate.name, intro, position.name, position.location, salary_change, position.salary_anual, description, skills, signature)

	# Record the MIME types of both parts - text/plain and text/html.
	
	part1 = MIMEText(text.encode('utf-8'), 'plain', 'utf-8')
	part2 = MIMEText(html.encode('utf-8'), 'html', 'utf-8')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)

	# Send the mail
	# send_mail('Job opportunity!', 'please', recruiter.email, TO, fail_silently=False, auth_user=recruiter.email, connection=None, html_message=html)
	
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

def single_candidate(request, candidate_id):
	candidate = get_object_or_404(Candidate, id=candidate_id)
	position = candidate.position
	block = {'candidate':candidate, 'position':position}
	return render(request, 'single_candidate.html', block)
