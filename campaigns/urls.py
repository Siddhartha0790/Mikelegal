from django.urls import path
from .views import SubscriberListCreateView, UnsubscribeView, CampaignListCreateView

urlpatterns = [
    path('subscribers/', SubscriberListCreateView.as_view(), name='subscriber-list-create'),
    path('unsubscribe/', UnsubscribeView.as_view(), name='unsubscribe'),
    path('campaigns/', CampaignListCreateView.as_view(), name='campaign-list-create'),
]
