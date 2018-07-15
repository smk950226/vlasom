from django.contrib import admin

from .models import Like

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'contents']
    list_display_links = ['user', 'contents']
    search_field = ['user', 'contents']
    list_filter = ['contents']
