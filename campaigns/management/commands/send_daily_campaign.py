import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from campaigns.models import Campaign
from campaigns.services.dispatcher import CampaignDispatcher

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Dispatches daily email campaigns using parallel processing.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--workers',
            type=int,
            default=10,
            help='Number of concurrent workers for dispatching campaigns',
        )

    def handle(self, *args, **options):
        workers = options['workers']
        # fetch campaigns
        today = timezone.now().date()
        
        # match date
        campaigns = Campaign.objects.filter(published_date__date=today)
        
        if not campaigns.exists():
            self.stdout.write(self.style.WARNING("No campaigns scheduled for today."))
            return
            
        self.stdout.write(self.style.SUCCESS(f"Found {campaigns.count()} campaigns scheduled for today."))
        
        dispatcher = CampaignDispatcher(max_workers=workers)
        
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
