# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags


# subject = 'Your One-Time Password (OTP)'
# html_message = render_to_string('twofactors.html',
#                                     {'otp_token': otp_token})
# plain_message = strip_tags(html_message)
# from_email = 'noreply-auth.core@grdflo.com'
# recipient_list = [email]
# email = EmailMultiAlternatives(subject, plain_message, from_email,
#                                    recipient_list)
# email.attach_alternative(html_message, "text/html")
# email.send()


from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import smtplib
from core.settings import auth, sender,EMAIL_HOST, EMAIL_PORT
from email.mime.text import MIMEText

def send_plain_text_email(subject, to_email, message, **kwargs):
    """Send a plain text email."""
    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email="hello@seoculus.com",
        to=[to_email],  # Recipient's email address(es)
    )

    email.send()

def Send_email_with_zoho_server(to_email, message):
     print('hello you!')
     msg = MIMEText(message)
     msg['Subject'] = "OTP from First Collectionz"
     msg['From'] = sender
     to=[to_email],  

     server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
     server.login(sender, auth)
     server.sendmail(sender, to,  msg.as_string())

     server.quit()
    
     