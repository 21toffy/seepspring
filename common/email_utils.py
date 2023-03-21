from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


import requests

class SendChampEmailSender:
    def __init__(self):
        self.authorization = settings.SENDCHAMP_AUTHORIZATION
        self.url = settings.SENDCHAMP_EMAIL_URL
        self.sender_id = settings.SENDCHAMP_SENDER_ID
        self.headers = {"accept": "application/json","content-type": "application/json", "Authorization":"Bearer " + self.authorization}

    
    def send_email(self, subject, to_email, to_name, from_email, from_name, message_body_type, message_body_value):
        payload = {
            "subject": subject,
            "to": [
                {
                    "email": to_email,
                    "name": to_name
                }
            ],
            "from": {
                "email": from_email,
                "name": from_name
            },
            "message_body": {
                "type": message_body_type,
                "value": message_body_value
            }
        }
        try:

            response = requests.post(self.url, json=payload, headers=self.headers)
            print(response.json(), "9999999999999999999999999999999999999")
            return response.json()
        except Exception as e:
            return  {
                    "data": None,
                    "message": f"Something went wrong {str(e)}",
                    "status": 400,
                    "code": 400
                    } 




def send_email(subject, to_email, context, template_name, html_template_name=None, from_email=None):
    """
    Send email to the specified recipient.
    """
    from_email = from_email or settings.EMAIL_HOST_USER

    # Render the plain text email content from the template
    text_content = render_to_string(template_name, context)
    # Remove HTML tags to create a plain text version of the email content
    plain_text_content = strip_tags(text_content)

    # Create the email message object with the plain text content
    email = EmailMultiAlternatives(subject, plain_text_content, from_email, [to_email])

    # If an HTML template name is specified, render the HTML email content from the template
    if html_template_name:
        html_content = render_to_string(html_template_name, context)
        email.attach_alternative(html_content, 'text/html')

    # Send the email
    email.send()
