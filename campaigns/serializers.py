from rest_framework import serializers
from .models import Subscriber, Campaign

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['id', 'email', 'first_name', 'is_active', 'subscribed_at', 'unsubscribed_at']
        read_only_fields = ['id', 'is_active', 'subscribed_at', 'unsubscribed_at']

    def create(self, validated_data):
        email = validated_data.get('email')
        # prevent duplicates
        if Subscriber.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "This email is already subscribed."})
        return super().create(validated_data)

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
