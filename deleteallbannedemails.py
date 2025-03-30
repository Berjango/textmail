#NO GUARANTEE THIS PROGRAM DOES ANYTHING USEFUL OR SAFE
#USE AT OWN RISK


#deletes all banned emails

##################################    CONFIGURATION SECTION ,change values as required ########################
debug=0 # if set to  1 the program will print extra information useful for debugging
################################################################################################################


import poplib
poplib._MAXLINE=20480
import email
from email.parser import Parser
import re
import utils
import datetime
from getpass import getpass



while not utils.internet_on():
	key=input("No internet connection. Connect computer to the internet and press Enter, or e(x)it, or (c)ontinue anyway -> ")
	if(key.upper()=="X"):
		exit()
	elif(key.upper()=="C"):
		break
try:
	dat=open(utils.bannedfile,"r")
	banned=dat.read().split()
	dat.close()
	if debug:
		print("Banned parts of email addresses - > "+str(banned))
except:
	ban=[]
	print("No banned addresses detected. You can create a file called banned and list banned addresses in the consecutive lines\n")
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
if len(emailaddress)<3:
	emailaddress,server,password=utils.typeinboxdetails()
else:
	password=getpass("Type the email password -> ")
#p=Parser()
loggedin=0
while not loggedin:
	try:
		pop = poplib.POP3(server)#pop3 account (hostname)
		pop.user(emailaddress)#user name (first part of email adress
		pop.pass_(password)#Email password
		messagecount, mailsize = pop.stat()
		loggedin=1
	except:
		choice=input("Could not login to inbox,probably wrong details.Type m to enter details manually,p to enter password again or press enter to exit.\n")
		if (choice.upper()=="M"):
			emailaddress,server,password=utils.typeinboxdetails()
		elif(choice.upper()=="P"):
			password=getpass("Type the email password -> ")
		else:
			exit(1)

emailsdeleted=0
for n in range(1,messagecount):
	response, lines, octets = pop.retr(n)
	details=utils.emaildetails(lines)
	if(utils.inlist(details[0],banned)):
		print("Email number "+str(n)+" is banned and will be deleted\n")
		pop.dele(n)
		emailsdeleted+=1
pop.quit()

print("Total emails deleted = "+str(emailsdeleted)+"\n")


