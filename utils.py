
import re

def	html2text(html):
	text=re.sub(r'<.[^>]*>',"",html)
	text=re.sub(r'\'\, b\'\s*'," ",text)
	text=re.sub(r'=09'," ",text)
	return(text)


def inlist(text,thelist):
	for el in thelist:
		m=re.search(el,text)
		try:
			ans=m.span()
		except:
			ans=[0,0]
		if ans[0]!=0 or ans[1]!=0:
			return(1)
	return(0)

def	emaildetails(rawemail):
	fields=["From:.{0,80}<.{0,50}@.{0,50}>\,","Date:.{0,30}\d{2}:\d{2}:\d{2}.{0,30}\,","Subject:.{0,3}=.{5,150}\,"]
	r2=re.sub("\"","",str(rawemail))
	r2=re.sub("\'","",r2)
	output=[]
	for field in fields:
		mobj=re.search(field,r2)
		if mobj:
			output.append(mobj.group())
	return(output)
