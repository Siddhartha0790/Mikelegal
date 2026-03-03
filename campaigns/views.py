from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.utils import timezone
from .models import Subscriber, Campaign
from .serializers import SubscriberSerializer, CampaignSerializer

class SubscriberListCreateView(generics.ListCreateAPIView):
    """
    manage subscribers
    """
    serializer_class = SubscriberSerializer

    def get_queryset(self):
        return Subscriber.objects.filter(is_active=True)

class UnsubscribeView(APIView):
    """
    deactivate subscriber
    """
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            subscriber = Subscriber.objects.get(email=email)
            if not subscriber.is_active:
                return Response({"message": "Subscriber is already unsubscribed."}, status=status.HTTP_200_OK)
            
            subscriber.is_active = False
            subscriber.unsubscribed_at = timezone.now()
            subscriber.save()
            return Response({"message": "Successfully unsubscribed."}, status=status.HTTP_200_OK)
        except Subscriber.DoesNotExist:
            return Response({"error": "Subscriber with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

class CampaignListCreateView(generics.ListCreateAPIView):
    """
    manage campaigns
    """
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [IsAdminUser]
