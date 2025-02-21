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
import re
from getpass import getpass

emailstoprint=15
todelete=[]
def	printdetails(rawtext):
	fields=["From:.{0,80}<.{0,50}@.{0,50}>\,","Date:.{0,30}\d{2}:\d{2}:\d{2}.{0,30}\,","Subject:.{0,3}=.{5,150}\,"]
	r=str(rawtext)
	r2=re.sub("\"","",r)
	r2=re.sub("\'","",r2)
	for field in fields:
		mobj=re.search(field,r2)
		if mobj:
			print(mobj.group())

try:
    dat=open("inboxdata")
    emailaddress=dat.readline().strip()
    server=dat.readline().strip()
    dat.close()
    print("Saved email address = "+emailaddress+" saved inbox server = "+server+"\n")
except:
    emailaddress=""
    server=""
    print("No saved data. You can create a text file named inboxdata to save time with the first line containing the email address and second line the inbox server\n")

#p=Parser()
if len(emailaddress)<3:
    emailaddress=input("Type the email address -> ")
if len(server)<3:
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
		print (em)
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
