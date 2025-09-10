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
deleteforeignemails=1 # if set to 1 deletes emails with non English language in the from field
################################################################################################################


import poplib
poplib._MAXLINE=20480
import email
from email.parser import Parser
import re
import utils
import datetime
from getpass import getpass


todelete=[]



def savedelemail(data,number):
	'''prepares to delete an email and saves it'''
	todelete.append(number)
	utils.savemail(data,number)


while not utils.internet_on():
	key=input("No internet connection. Connect computer to the internet and press Enter, or e(x)it, or (c)ontinue anyway -> ")
	if(key.upper()=="X"):
		exit()
	elif(key.upper()=="C"):
		break
banned=utils.textfiletolist(utils.bannedfile)
if(not len(banned)):
	print("No banned addresses detected. You can create a file called banned and list banned addresses in the consecutive lines.\n")
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
	firstfield=details[0]
	isfromfield=re.search("From:",firstfield)
	foreign=re.search("=",firstfield)
	if not isfromfield:
		print("From field too long,likely spam or malformed email,will delete.\n")
		savedelemail(em,emailnumber)
		emailnumber-=1		
		continue
	elif isfromfield and foreign and deleteforeignemails:
		utils.printdetails(details)
		x1=input("Foreign language detected in from field,will delete.press n for don't delete.'\n")
		if(x1.upper()!="N"):
			savedelemail(em,emailnumber)
			emailnumber-=1
			continue
	else:
		utils.printdetails(details)
	if(utils.inlist(firstfield,banned)):
		print("This email address is banned and will be deleted\n")
		savedelemail(em,emailnumber)
		emailnumber-=1		
		continue
	choice=input("Print raw message? (Y)es,(D)elete email,(B)an email address and delete,(S)ave email , E(x)it or Press Enter to see next email. -> ")
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
			savedelemail(em,emailnumber)
	elif(choice.upper()=="B"):
		data=re.split("@",details[0])[1]
		if(debug):
			print("From field= "+details[0]+"    data= "+data+"\n")
		data=re.sub(r'>.*',"",data)
		try:
			if(debug):
				print(data)
			dat=open(utils.bannedfile,"a")
			dat.write(data+"\n")
			dat.close()
			savedelemail(em,emailnumber)
			print("Banned email "+str(emailnumber)+"\n")
		except:
			print("Could not add banned email address,try adding it manually in a text editor\n")
	elif (choice.upper()=="D"):
		wait=input("\n\nWill delete email number "+str(emailnumber)+"   Press n to not delete or Enter to continue -> ")
		if (wait.upper()!="N"):
			savedelemail(em,emailnumber)

	elif(choice.upper()=="X"):
		break
	elif(choice.upper()=="S"):
		utils.savemail(em,emailnumber)

	emailnumber-=1

todelete+=range(1,messagecount-maximumemails-len(todelete)+1)
if(debug):
    print("todelete = "+str(todelete))

if todelete:
	utils.delete_emails(todelete,server,emailaddress,password)

