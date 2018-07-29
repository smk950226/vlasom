from django.contrib import admin

from .models import Category, Contents, ContentsImages


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'interest_count']
    ordering = ['-interest_count']


@admin.register(Contents)
class ContentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'category_1', 'views', 'like_count', 'interest_count']
    list_display_links = ['id', 'user', 'category_1']
    search_field = ['user__username', 'category_1']
    list_filter = ['user', 'category_1']
    ordering = ['-id', '-views', '-like_count', '-interest_count']


@admin.register(ContentsImages)
class ContentsImagesAdmin(admin.ModelAdmin):
    list_display = ['contents']