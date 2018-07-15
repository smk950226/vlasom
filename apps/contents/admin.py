from django.contrib import admin

from .models import Category, Contents, ContentsImages, Like


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Contents)
class ContentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'category_1', 'views', 'like_count']
    list_display_links = ['id', 'user', 'category_1']
    search_field = ['user__username', 'category_1']
    list_filter = ['user', 'category_1']
    ordering = ['-id', '-views', '-like_count']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'contents']
    list_display_links = ['user', 'contents']
    search_field = ['user', 'contents']
    list_filter = ['contents']

