from django.urls import path
from .views import SubscriberListCreateView, UnsubscribeView

urlpatterns = [
    path('subscribers/', SubscriberListCreateView.as_view(), name='subscriber-list-create'),
    path('unsubscribe/', UnsubscribeView.as_view(), name='unsubscribe'),
]
