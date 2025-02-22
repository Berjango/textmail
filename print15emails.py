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
import utils
from getpass import getpass

emailstoprint=15
todelete=[]


    
try:
    dat=open("banned")
    banned=(dat.read().split("\n"))
    print(banned)
except:
    banned=[]
    print("No banned addresses detected. You can create a file called banned and list banned addresses in the lines\n")
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
try:
	pop = poplib.POP3(server)#pop3 account (hostname)
	pop.user(emailaddress)#user name (first part of email adress
	pop.pass_(password)#Email password
	messagecount, mailsize = pop.stat()
except:
	print("Could not login to inbox,probably wrong details.Check login details.\n")
	messagecount=0
if(messagecount==0):
	exit(1)

emails=[]
for n in range(messagecount,messagecount-emailstoprint,-1):
	response, lines, octets = pop.retr(n)
	emails.append(lines)
pop.quit()
emailnumber=messagecount
for em in emails:
	print("\nEMAIL number "+str(emailnumber)+"\n")
	details=utils.emaildetails(em)
	for info in details:
			print(info)
	if(utils.inlist(details[0],banned)):
		print("This email address is banned and will be deleted\n")
		todelete.append(emailnumber)
		emailnumber-=1		
		continue
	choice=input("Print raw message? (Y)es or (N)o ,(D)elete email,(S)ave email or E(x)it -> ")
	if (choice.upper()=="Y"):
		print (utils.html2text(str(em)))
		print("\n\n\n\n")
#		wait=input("\n\nEnd of message. Press Enter to continue")
	elif (choice.upper()=="D"):
		wait=input("\n\nWill delete email number "+str(emailnumber)+"   Press n to not delete or Enter to continue -> ")
		if (wait.upper()!="N"):
			todelete.append(emailnumber)
	elif(choice.upper()=="X"):
		break			
	elif(choice.upper()=="S"):
		filename="email"+str(emailnumber)+".eml"
		try:
			f=open(filename,"w")
			f.write(str(em))
			f.close()
			print("Saved email as "+filename+"\n")
		except:
			print("Error! Could not save email\n")

	emailnumber-=1
if not todelete:
	exit(0)
pop = poplib.POP3(server)#pop3 account (hostname)
pop.user(emailaddress)#user name (first part of email adress
pop.pass_(password)#Email password
x=pop.stat()
for id in todelete:
	print("Deleting email "+str(id)+"\n")
	pop.dele(id)
pop.quit()
