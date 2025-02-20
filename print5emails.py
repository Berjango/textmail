#NO GUARANTEE THIS PROGRAM DOES ANYTHING USEFUL OR SAFE
#USE AT OWN RISK
#Lightweight program to print the last few emails as text!!
# This is a poorly writte program to roughly work
#Peter Wolf 15-12-2023
#Does not do html or follow links
#Updated 17 Feb 2025 (roughly working on this date))
import poplib
import email
from email.parser import Parser
import os
import sys


def	printdetails(rawtext):
	r=str(rawtext)
	i=r.find("From:")
	print("FROM : "+str(r[i+7:i+60]))
	i=r.find("Date:")
	print("DATE : "+str(r[i+7:i+60]))
	i=r.find("Subject:")
	print("SUBJECT:"+str(r[i+8:i+68])+"\n\n")


#p=Parser()
emailaddress=input("Type the email address -> ")
server=input("Type the incoming mail server address -> ")
password=input("Type the email password -> ")
pop = poplib.POP3(server)#pop3 account (hostname)
pop.user(emailaddress)#user name (first part of email adress
pop.pass_(password)#Email password
messagecount, mailsize = pop.stat()
emails=[]
for n in range(messagecount,messagecount-15,-1):
	response, lines, octets = pop.retr(n)
	emails.append(lines)
pop.quit()

for email in emails:
	printdetails(email)
#	emailstr=str(lines)
	#emailMessage=p.parsestr(emailstr)
#msgJustHeaders = p.parsestr(nbMsg, True)
#emailMessage = email.message_from_string(nbMsg)
#fields = emailMessage.keys()
	#fromaddress=str(emailMessage.__getitem__("From"))
	#subj = str(emailMessage.__getitem__("Subject"))
#	print ("from"+fromaddress+" subj="+subj+"\n\n")
	#print(emailMessage)
	choice=input("Print raw message? (Y)es or (N)o -> ")
	if (choice=="Y" or choice=="y"):
		print (email)
		print("\n\n\n\n")
		wait=input("\n\nEnd of message. Press Enter to continue")
#print ("The message contains the following keys:\n")
#for field in fields:
#	print (field + "\n")

