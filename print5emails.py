#NO GUARANTEE THIS PROGRAM DOES ANYTHING USEFUL OR SAFE
#USE AT OWN RISK
#Lightweight program to print the last few emails as text!!
#Peter Wolf 15-12-2023
#Does not do html or follow links
#Updated 17 Feb 2025 (roughly working on this date))
import poplib
#from email.Parser import Parser
import email
import os
import sys
emailaddress=input("Type the email address -> ")
server=input("Type the incoming mail server address -> ")
password=input("Type the email password -> ")
pop = poplib.POP3(server)#pop3 account (hostname)
pop.user(emailaddress)#user name (first part of email adress
pop.pass_(password)#Email password
nbMsg, nbOctet = pop.stat()
emailstr=""
for n in range(nbMsg):
	response, lines, bytes = pop.retr(n+1)
	emailstr+=str(lines[n+1])
	print (response,lines,bytes)
print ("retrieved email")
# which retrieve email from a pop3 account and
p=Parser()
emailMessage=p.parsestr(emailstr)
#msgJustHeaders = p.parsestr(nbMsg, True)
#emailMessage = email.message_from_string(nbMsg)
fields = emailMessage.keys()
#if (emailMessage.has_key(‘To’)):
#print "has keys"
#	emailMessage.__delitem__(‘To’)
#fromaddress=emailMessage.__getitem__(‘From’)
#emailMessage.__setitem__(‘To’, ‘test@yourdomain.com’)
subj = emailMessage.__getitem__("Subject")
print ("The message contains the following keys:\n")
for field in fields:
	print (field + "\n")
print ("from"+fromaddress+" subj="+subj)
