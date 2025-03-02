
import re

def	html2text(html):
	'''A very simplistic and rough html to text converter'''
	todelete=[r'<.[^>]*>',r'\'\, b\'\s*',r'=[a-zA-z0-9]{2}\s*',r'\{.[^\}]*\}',r'https?.[^\s]*',r'[a-zA-Z0-9]{20,200}']
	text=html
	for el in todelete:
		text=re.sub(el," ",text)
	return(text)


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
	fields=["From:.{0,80}<.{0,50}@.{0,50}>\,","Date:.{0,30}\d{2}:\d{2}:\d{2}.{0,30}\,","Subject:.{0,3}=.{5,150}\,"]
	r2=re.sub("\"","",str(rawemail))
	r2=re.sub("\'","",r2)
	output=[]
	for field in fields:
		mobj=re.search(field,r2)
		if mobj:
			output.append(mobj.group())
	return(output)

