
import re
from getpass import getpass
import poplib
poplib._MAXLINE=20480
import datetime

bannedfile="banned"


def	savemail(emaildata,emailnumber):
	''' Save email to the temp folder with a unique name'''
	filename="/tmp/email"+str(emailnumber)+"_"+str(datetime.datetime.now())+".eml"
	try:
		f=open(filename,"w")
		f.write(str(emaildata))
		f.close()
		print("Temporarily saved email as "+filename+"\n")
	except:
		print("Error! Could not save email\n")

def	html2text(html):
	'''A very simplistic and rough html to text converter'''
	todelete=[r'<.[^>]*>',r'\'\, b\'\s*',r'=[a-zA-z0-9]{2}\s*',r'\{.[^\}]*\}',r'https?.[^\s]*',r'[a-zA-Z0-9]{20,200}',r'\&nbsp\;',r'\&\#.[\s]*',r'\.wrapper',r'\.colspan.[^\s]*',r'\.container.[^\s]*',r'\\x.[^\s]*',r'\\t',r'[\s=\-\,_bFE\;]{5,1000}']
	text=html
	for el in todelete:
		text=re.sub(el," ",text)
	return(text)
from urllib import request

def internet_on():
	if(openurl("https://google.com")):
		return	True
	elif(openurl("https://yahoo.com")):
		return	True
	else:
		return	False
def	typeinboxdetails():
	emailaddress=input("Type the email address -> ")
	server=input("Type the incoming mail server address -> ")
	password=getpass("Type the email password -> ")
	return(emailaddress,server,password)
	
def delete_emails(todelete,server,emailaddress,password):
	'''deletes emails according to a passed list of email numbers'''
	try:
		pop = poplib.POP3(server)#pop3 account (hostname)
		pop.user(emailaddress)#user name (first part of email adress
		pop.pass_(password)#Email password
		print("Preparing to delete\n")
		for id in todelete:
			print("Deleting email "+str(id)+"\n")
			pop.dele(id)
		pop.quit()
	except:
		print("Unable to delete emails,probably a temporary login problem,next time should work.\n")


def	openurl(theurl):
	try:
		request.urlopen(theurl, timeout=1)
		return True
	except request.URLError as err: 
		return False


def inlist(text,thelist):
	'''Returns true if only if the text is embeded in a list element'''
	for el in thelist:
		m=re.search(el,text)
		try:
			ans=m.span()
		except:
			ans=[0,0]
		if ans!=[0,0]:
			return(1)
	return(0)

def	emaildetails(rawemail):
	'''Returns a list of email details '''
	fields=["From:.[^<]{0,140}<.[^>]{0,100}>\,","Date:.{0,30}\d{2}:\d{2}:\d{2}.{0,30}\,","Subject:.{0,3}=.[^\,]{5,150}\,","Content\-Type:.*"]
	r2=re.sub("\"","",str(rawemail))
	r2=re.sub("\'","",r2)
	output=[]
	for field in fields:
		mobj=re.search(field,r2)
		if mobj:
			output.append(mobj.group())
	return(output)

