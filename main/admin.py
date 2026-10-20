from django.contrib import admin

from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('title', 'channel_name', 'card_type', 'published', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('card_type', 'is_active', 'channel_name')
    search_fields = ('title', 'video_id')
    date_hierarchy = 'published'
