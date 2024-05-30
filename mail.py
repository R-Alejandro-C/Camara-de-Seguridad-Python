import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib

load_dotenv()
password = os.getenv("PASSWORD")
email_from = "kailer.3000.11@gmail.com"
email_to = "kailer.3000.11@gmail.com"

subject = "Te estan robando!!!... Tal vez..."
body = """Es posible que alguien este en tu domicilio"""

em = EmailMessage()

em["From"] = email_from
em["To"] = email_to
em["Subject"] = subject
em.set_content(body)

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com",465, context=context) as smtp:
    smtp.login(email_to, password)
    smtp.sendmail(email_to, email_from, em.as_string()) 



