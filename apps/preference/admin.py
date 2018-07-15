from django.contrib import admin

from .models import Like, Interest

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'contents']
    list_display_links = ['user', 'contents']
    search_field = ['user', 'contents']
    list_filter = ['contents']


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ['user', 'contents', 'category']
    list_display_links = ['user', 'contents', 'category']
    search_field = ['user', 'contents', 'category']
    list_filter = ['category']