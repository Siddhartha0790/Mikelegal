import logging
from decouple import config
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

logger = logging.getLogger(__name__)

def send_email(subscriber, campaign):
    """
    Sends an email to a subscriber for a given campaign.
    Uses Django's EmailMultiAlternatives to send both plain text and HTML.
    Falls back to dummy logic if EMAIL_HOST is not configured or in tests.
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
    
    # Optional: Build a better plain text version using the template or use the provided one
    plain_message = f"Hi {subscriber.first_name},\n\n{campaign.plain_text_content}\n\nRead more at: {campaign.article_url}\n\nUnsubscribe: {context['unsubscribe_url']}"
    
    try:
        if settings.EMAIL_HOST == 'dummy' or not settings.EMAIL_HOST:
            # Dummy successful send
            logger.info(f"[DUMMY] Email sent to {subscriber.email} for campaign '{campaign.subject}'")
            return True, None

        msg = EmailMultiAlternatives(
            subject=campaign.subject,
            body=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[subscriber.email]
        )
        msg.attach_alternative(html_message, "text/html")
        msg.send(fail_silently=False)
        return True, None
        
    except Exception as e:
        logger.error(f"Failed to send email to {subscriber.email}: {str(e)}")
        return False, str(e)
