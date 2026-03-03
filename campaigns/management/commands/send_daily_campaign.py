import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from campaigns.models import Campaign
from campaigns.services.dispatcher import CampaignDispatcher

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Dispatches daily email campaigns using parallel processing.'

    def handle(self, *args, **options):
        # Fetch campaigns where published_date is today
        # Note: timezone.now().date() represents the current date
        today = timezone.now().date()
        
        # We find campaigns whose published_date matches today's date
        # using __date lookup
        campaigns = Campaign.objects.filter(published_date__date=today)
        
        if not campaigns.exists():
            self.stdout.write(self.style.WARNING("No campaigns scheduled for today."))
            return
            
        self.stdout.write(self.style.SUCCESS(f"Found {campaigns.count()} campaigns scheduled for today."))
        
        dispatcher = CampaignDispatcher(max_workers=10)
        
        for campaign in campaigns:
            self.stdout.write(f"Starting dispatch for campaign: {campaign.subject}")
            
            results = dispatcher.dispatch(campaign)
            
            self.stdout.write(self.style.SUCCESS(
                f"\n--- Campaign Summary: '{campaign.subject}' ---\n"
                f"Total Subscribers Expected: {results['total']}\n"
                f"Successfully Sent: {results['sent']}\n"
                f"Failed: {results['failed']}\n"
                "------------------------------------------------"
            ))
            
        self.stdout.write(self.style.SUCCESS("All daily campaigns dispatched successfully."))
