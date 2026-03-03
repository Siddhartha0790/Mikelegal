from django.contrib import admin
from .models import Subscriber, Campaign, CampaignLog

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'is_active', 'subscribed_at', 'unsubscribed_at')
    list_filter = ('is_active',)
    search_fields = ('email', 'first_name')

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('subject', 'published_date', 'created_at')
    list_filter = ('published_date',)
    search_fields = ('subject', 'preview_text')

@admin.register(CampaignLog)
class CampaignLogAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'subscriber', 'status', 'sent_at')
    list_filter = ('status', 'sent_at')
    search_fields = ('subscriber__email', 'campaign__subject')
