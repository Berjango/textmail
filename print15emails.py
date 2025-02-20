#NO GUARANTEE THIS PROGRAM DOES ANYTHING USEFUL OR SAFE
#USE AT OWN RISK
#Lightweight program to print the last few emails as text!!
# This is a poorly written program to roughly work
#Peter Wolf 15-12-2023
#Does not do html or follow links
#Updated 17 Feb 2025 (roughly working on this date))
import poplib
import email
from email.parser import Parser
import os
from getpass import getpass

emailstoprint=15
todelete=[]
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
password=getpass("Type the email password -> ")
pop = poplib.POP3(server)#pop3 account (hostname)
pop.user(emailaddress)#user name (first part of email adress
pop.pass_(password)#Email password
messagecount, mailsize = pop.stat()
emails=[]
for n in range(messagecount,messagecount-emailstoprint,-1):
	response, lines, octets = pop.retr(n)
	emails.append(lines)
pop.quit()
emailnumber=messagecount
for em in emails:
	print("\nEMAIL number "+str(emailnumber)+"\n")
	printdetails(em)
	#msg = email.message_from_bytes(em)
#	emobj=p.parsestr(str(em))
#msgJustHeaders = p.parsestr(nbMsg, True)
#emailMessage = email.message_from_string(nbMsg)
#fields = emailMessage.keys()
#	fromaddress=str(emobj.__getitem__("From"))
#	subj = str(emobj.__getitem__("Subject"))
#	print("From:"+fromaddress+" Subject:"+subj+"\n\n")
	#print(msg)
	#print(emailMessage)
	choice=input("Print raw message? (Y)es or (N)o (D)elete message or (E)xit -> ")
	if (choice.upper()=="Y"):
		print (email)
		print("\n\n\n\n")
		wait=input("\n\nEnd of message. Press Enter to continue")
	elif (choice.upper()=="D"):
		wait=input("\n\nWill delete email number "+str(emailnumber)+"   Press n to not delete or Enter to continue")
		if (wait.upper()!="N"):
			todelete.append(emailnumber)
	elif(choice.upper()=="E"):
		break			
	emailnumber-=1
#print ("The message contains the following keys:\n")
#for field in fields:
#	print (field + "\n")
pop = poplib.POP3(server)#pop3 account (hostname)
pop.user(emailaddress)#user name (first part of email adress
pop.pass_(password)#Email password
x=pop.stat()
for id in todelete:
	print("Deleting email "+str(id)+"\n")
	pop.dele(id)
pop.quit()
