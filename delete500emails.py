#NO GUARANTEE THIS PROGRAM DOES ANYTHING USEFUL OR SAFE
#USE AT OWN RISK

#Program designed to delete first 500 emails on a pop email server for the purpose of making more room
import poplib
import email
from email.parser import Parser
import os
from getpass import getpass

emailstodelete=500

emailaddress=input("Type the email address -> ")
server=input("Type the incoming mail server address -> ")
password=getpass("Type the email password -> ")
pop = poplib.POP3(server)#pop3 account (hostname)
pop.user(emailaddress)#user name (first part of email adress
pop.pass_(password)#Email password
messagecount, mailsize = pop.stat()
print("Current message count = "+str(messagecount)+"Current mailsize = "+str(mailsize)+"\n")
for n in range(1,emailstodelete):
    print("Deleting email number "+str(n)+"\n")
    pop.dele(n)
messagecount, mailsize = pop.stat()
print("New message count = "+str(messagecount)+"New mailsize = "+str(mailsize)+"\n")
pop.quit()
