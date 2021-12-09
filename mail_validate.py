def pozdrav():
		from datetime import datetime
		hodina = datetime.now().hour
		if hodina>=0 and hodina<10:
			return "Dobré ráno"
		elif hodina>=10 and hodina<=12:
			return "Dobré dopoledne"
		elif hodina>12 and hodina<=16:
			return "Dobré odpoledne"
		elif hodina>16 and hodina<=20:
			return "Dobrý podvečer"
		elif hodina>20 and hodina<=23:
			return "Dobrý večer"

def hash_f(slovo):
		"""SLouží pro vygenerování náhodné kombinace znaků, které budou poslány na email pro jeho konfirmaci"""
		import string
		import random
		l=list(slovo)
		a,b,tmp=str(l[0]),str(l[-1]),[]
		for i in range(len(slovo)-2):
			tmp+=[random.choice(string.ascii_letters)]
			tmp+=[random.choice(string.digits)]
			tmp+=[random.choice(string.punctuation)]
		return a+"".join(tmp)+b

def my_auth(word, customer_mail_adress):

	def mail_sender(sec_key,customer_mail_adress,name):
	
		import os
		import smtplib
		from email.message import EmailMessage

		SENDER_PASSWORD = os.environ.get("EMAIL_PASS")
		SENDER_EMAIL = os.environ.get("EMAIL_USERNAME")
		msg=EmailMessage()
		
		msg['Subject']= "MRmHolub: Potvrzení Emailu"
		msg['From'] = SENDER_EMAIL
		msg['To'] = customer_mail_adress
		msg.set_content(str(pozdrav())+" " +str(name)+",\n z důvodu vyplnění registračního formuláře na webu www.MRmHolub.cz, Vám zasíláme kod pro potvrzení validace zadaného emailu.\n\n Kód: "+str(sec_key)+"\n\n Pokud jste žádný formulář nevyplňovali, prosím ignorujte tuto zprávu.\n\n\n Děkujeme, Team Holubů")
		
		with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
			smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
			smtp.send_message(msg)
	

	secret_key=hash_f(word)
	mail_sender(secret_key,customer_mail_adress,word)
	return secret_key



def new_username(customer_mail_adress,old_name,new_name):
	import os
	import smtplib
	from email.message import EmailMessage

	SENDER_PASSWORD = os.environ.get("EMAIL_PASS")
	SENDER_EMAIL = os.environ.get("EMAIL_USERNAME")
	msg=EmailMessage()
	
	msg['Subject']= "MRmHolub: Změna jména"
	msg['From'] = SENDER_EMAIL
	msg['To'] = customer_mail_adress
	msg.set_content(str(pozdrav())+" " +str(old_name)+",\n z důvodu změny vašeho jména na "+new_name+" na webu www.MRmHolub.cz, Vám zasíláme potvrzení o proběhnutí této záležiosti.\n\n Pokud jste žádné jméno neměnili, prosím okamžitě nás kontaktuje na čísle +420 610 096 228.\n\n\n Děkujeme že jste s námi, Team Holubů!")
	
	with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
		smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
		smtp.send_message(msg)
		#uzivatel je prihlasen jen po dobu co se posila zprava pak se automaticky odhlasi


def new_mail(customer_mail_adress,name):
	import os
	import smtplib
	from email.message import EmailMessage

	SENDER_PASSWORD = os.environ.get("EMAIL_PASS")
	SENDER_EMAIL = os.environ.get("EMAIL_USERNAME")
	msg=EmailMessage()
	
	msg['Subject']= "MRmHolub: Změna Emailu"
	msg['From'] = SENDER_EMAIL
	msg['To'] = customer_mail_adress
	sk=hash_f(name)
	msg.set_content(str(pozdrav())+" Vážený/á pane/paní, " +str(old_name)+",\n dostali jsme požadavek na změnu vašeho emailu na webu www.MRmHolub.cz, z tohoto důvodu Vám zasíláme Kod sloužící pro potvrzení.\n\n Kód: "+str(sk)+"\n\n Pokud jste nežádali o změnu emailu, neprodleně nád prosím kontaktuje na čísle +420 610 096 228.\n\n\n Děkujeme že jste s námi, Team Holubů!")
	
	with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
		smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
		smtp.send_message(msg)

	return sk