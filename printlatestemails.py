#NO GUARANTEE THIS PROGRAM DOES ANYTHING USEFUL OR SAFE
#USE AT OWN RISK
#Lightweight program to print and or process the last few emails!!
# This is a poorly written program to roughly work
#Peter Wolf 15-12-2023
#Does not do html or follow links
#Updated 17 Feb 2025 (roughly working on this date))



##################################    CONFIGURATION SECTION ,change values as required ########################
emailstoprint=15
maximumemails=2500 #Will autodelete oldest emails if the number of emails exceeds this value
debug=0 # if set to  1 the program will print extra information useful for debugging
maximumemailtext=15000#maximum allowed length of email text in chars after processing
################################################################################################################


import poplib
poplib._MAXLINE=20480
import email
from email.parser import Parser
import re
import utils
import datetime
from getpass import getpass


def delete_emails(todelete,server,emailaddress,password):
	'''deletes emails according to a passed list of email numbers'''
	try:
		pop = poplib.POP3(server)#pop3 account (hostname)
		pop.user(emailaddress)#user name (first part of email adress
		pop.pass_(password)#Email password
		print("\n")
		for id in todelete:
			print("Deleting email "+str(id)+"\n")
			pop.dele(id)
		pop.quit()
	except:
		print("Unable to delete emails,probably a temporary login problem,next time should work.\n")


def	typeinboxdetails():
	emailaddress=input("Type the email address -> ")
	server=input("Type the incoming mail server address -> ")
	password=getpass("Type the email password -> ")
	return(emailaddress,server,password)


todelete=[]
bannedfile="banned"

while not utils.internet_on():
	key=input("No inernet connection. Connect computer to the internet and press Enter, or e(x)it, or (c)ontinue anyway -> ")
	if(key.upper()=="X"):
		exit()
	elif(key.upper()=="C"):
		break
try:
	dat=open(bannedfile,"r")
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
	emailaddress,server,password=typeinboxdetails()
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
			emailaddress,server,password=typeinboxdetails()
		elif(choice.upper()=="P"):
			password=getpass("Type the email password -> ")
		else:
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
	text=details.pop(-1)
	for info in details:
			print(info)
	if(utils.inlist(details[0],banned)):
		print("This email address is banned and will be deleted\n")
		todelete.append(emailnumber)
		emailnumber-=1		
		continue
	choice=input("Print raw message? (Y)es,(D)elete email,(B)an email address and delete,(S)ave email or E(x)it -> ")
	if (choice.upper()=="Y"):
		emailtext=utils.html2text(str(text))
		if(len(emailtext)<maximumemailtext):
			print (emailtext)
			print("\n\n\n\n")
		else:
			ans=input("WARNING!!! Email text is too long,probably a scam email,recommended to not print and delete later.Press y to print anyway or enter to not print and continue. -> ")
			if(ans.upper()=="Y"):
				print (emailtext)
				print("\n\n\n\n")
	
		wait=input("\n\nEnd of message. Press (d) to delete or Enter to continue -> ")
		if(wait.upper()=="D"):
			todelete.append(emailnumber)
	elif(choice.upper()=="B"):
		data=re.split("@",details[0])[1]
		if(debug):
			print("From field= "+details[0]+"    data= "+data+"\n")
		data=re.sub(r'>.*',"",data)
		try:
			if(debug):
				print(data)
			dat=open(bannedfile,"a")
			dat.write(data+"\n")
			dat.close()
			todelete.append(emailnumber)
			print("Banned email "+str(emailnumber)+"\n")
		except:
			red_text("Could not add banned email address,try adding it manually in a text editor\n")
	elif (choice.upper()=="D"):
		wait=input("\n\nWill delete email number "+str(emailnumber)+"   Press n to not delete or Enter to continue -> ")
		if (wait.upper()!="N"):
			todelete.append(emailnumber)
	elif(choice.upper()=="X"):
		break			
	elif(choice.upper()=="S"):
		filename="email"+str(emailnumber)+"_"+str(datetime.datetime.now())+".eml"
		try:
			f=open(filename,"w")
			f.write(str(em))
			f.close()
			print("Saved email as "+filename+"\n")
		except:
			print("Error! Could not save email\n")

	emailnumber-=1

todelete+=range(1,messagecount-maximumemails-len(todelete)+1)
if(debug):
    print("todelete = "+str(todelete))

if todelete:
	delete_emails(todelete,server,emailaddress,password)

