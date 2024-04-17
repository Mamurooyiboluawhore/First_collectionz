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


def send_plain_text_email(subject, to_email, message, **kwargs):
    """Send a plain text email."""
    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email="mamurooyibo@gmail.com",
        to=[to_email],  # Recipient's email address(es)
    )

    email.send()