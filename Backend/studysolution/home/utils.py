from django.core.mail import EmailMessage
from django.conf import settings
import os

class Util:
    @staticmethod
    def send_email(data):
        try:
            # Create the email message
            email = EmailMessage(
                subject=data['subject'],
                body=data['body'],
                from_email=os.environ.get('EMAIL_FROM'),  # Ensure this is set in your environment
                to=[data['to_email']]
            )
            
            # Send the email
            email.send(fail_silently=False)  # Set to False to raise exceptions on errors
            
            print(f"Email sent to {data['to_email']} successfully.")
        except Exception as e:
            print(f"Error sending email: {e}")
