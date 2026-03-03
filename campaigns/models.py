from django.db import models
from django.utils import timezone
import uuid

class Subscriber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True, db_index=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.email} ({'Active' if self.is_active else 'Unsubscribed'})"


class Campaign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField(max_length=255)
    preview_text = models.CharField(max_length=255, blank=True)
    article_url = models.URLField()
    html_content = models.TextField()
    plain_text_content = models.TextField()
    published_date = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class CampaignLog(models.Model):
    STATUS_CHOICES = (
        ('SENT', 'Sent'),
        ('FAILED', 'Failed'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='logs')
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, related_name='logs')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    sent_at = models.DateTimeField(default=timezone.now)
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Log for {self.campaign.subject} to {self.subscriber.email} - {self.status}"
