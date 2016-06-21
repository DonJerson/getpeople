import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import webbrowser


FROM = recruiter.email
TO = [candidate.email] # must be a list

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Job opportunity!"
msg['From'] = recruiter.email
msg['To'] = candidate.email


description = """<pre>%s</pre>""" % (position.description)
skills = """<pre>%s</pre>""" % (position.skills)

intro = """My name is %s, I am a Staff Recruiter specialist from Barrister. We are a nation-wide agency filling full time job positions for some of the largest corporations in the US. I found your resume online and I believe you are a good candidate for a job opening we have. Down bellow you will find the job description, please reply back to this email if you are interested in this opportunity.""" % (recruiter.name)
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
""" % (candidate.name, intro, position.name, position.location, position.annual_salary, description, skills, signature)


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
server.login(self, 'Barrister123')
server.sendmail(FROM, TO, msg.as_string())
server.close()

