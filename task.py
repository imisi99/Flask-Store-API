from flask import current_app
from flask_mail import Message
import os
import requests
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv( "MAILGUN_DOMAIN")
def send_simple_message(to, subject, body):
	return requests.post(
		f"https://api.mailgun.net/v3/{DOMAIN}/messages",
		auth=("api", os.getenv( "MAILGUN_API_KEY")),
		data={"from": f"Bankai <mailgun@{DOMAIN}>", 
			"to": [to],
			"subject": subject,
			"text": body
			
            }
			
    )

def send_user_registration_email(email, username):
	return send_simple_message(
		email,
		"Successfully Signed up!",
		f"Hi {username} you have successfully signed up to the Stores API,"
    )

def send_email(subject, sender, recipients, username,  html= None):
	msg = Message(subject, sender= sender, recipients= recipients)
	msg.body = f"{username}, you have successfully created an account, We are Happy to have you onboard on this API "
	if  html:
		msg.html = html
	
	mail = current_app.extensions['mail']
	mail.send(msg)