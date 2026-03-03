import logging
from decouple import config
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

logger = logging.getLogger(__name__)

def send_email(subscriber, campaign):
    """
    send email
    """
    context = {
        'first_name': subscriber.first_name,
        'email': subscriber.email,
        'subject': campaign.subject,
        'preview_text': campaign.preview_text,
        'html_content': campaign.html_content,
        'article_url': campaign.article_url,
        'unsubscribe_url': f"http://localhost:8000/api/unsubscribe/?email={subscriber.email}" # Base URL should come from settings in prod
    }

    html_message = render_to_string('email/campaign.html', context)
    
    # build plaintext
    plain_message = f"Hi {subscriber.first_name},\n\n{campaign.plain_text_content}\n\nRead more at: {campaign.article_url}\n\nUnsubscribe: {context['unsubscribe_url']}"
    
    # dummy send
    logger.info(f"[DUMMY] Email sent to {subscriber.email} for campaign '{campaign.subject}'")
    print(f"\n--- DUMMY EMAIL TO {subscriber.email} ---")
    print(f"Subject: {campaign.subject}")
    print(f"{plain_message}")
    print("-------------------------------------------\n")
    return True, None
