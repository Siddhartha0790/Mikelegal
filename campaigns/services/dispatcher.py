import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.utils import timezone
from campaigns.models import Subscriber, CampaignLog
from .email_service import send_email

logger = logging.getLogger(__name__)

class CampaignDispatcher:
    def __init__(self, max_workers=10):
        # thread pool
        self.max_workers = max_workers

    def _process_subscriber(self, subscriber, campaign):
        """
        process subscriber
        """
        success, error_msg = send_email(subscriber, campaign)
        
        status = 'SENT' if success else 'FAILED'
        
        # log result
        CampaignLog.objects.create(
            campaign=campaign,
            subscriber=subscriber,
            status=status,
            sent_at=timezone.now(),
            error_message=error_msg
        )
        
        return success

    def dispatch(self, campaign):
        """
        dispatch campaign
        """
        # fetch subscribers
        subscribers = list(Subscriber.objects.filter(is_active=True))
        
        if not subscribers:
            logger.info(f"No active subscribers found for campaign {campaign.id}")
            return {'sent': 0, 'failed': 0, 'total': 0}

        sent_count = 0
        failed_count = 0
        
        logger.info(f"Dispatching campaign {campaign.id} to {len(subscribers)} subscribers using {self.max_workers} workers.")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # submit tasks
            future_to_subscriber = {
                executor.submit(self._process_subscriber, sub, campaign): sub 
                for sub in subscribers
            }
            
            # wait results
            for future in as_completed(future_to_subscriber):
                subscriber = future_to_subscriber[future]
                try:
                    success = future.result()
                    if success:
                        sent_count += 1
                    else:
                        failed_count += 1
                except Exception as exc:
                    logger.error(f"Worker generated an exception for {subscriber.email}: {exc}")
                    failed_count += 1
                    
                    # ensure log
                    CampaignLog.objects.create(
                        campaign=campaign,
                        subscriber=subscriber,
                        status='FAILED',
                        sent_at=timezone.now(),
                        error_message=str(exc)
                    )

        return {'sent': sent_count, 'failed': failed_count, 'total': len(subscribers)}
