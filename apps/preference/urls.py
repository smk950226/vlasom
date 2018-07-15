from django.urls import path
from . import views

app_name = 'preference'
urlpatterns = [
    path('like/<int:pk>/', views.like_create, name = 'like_create'),
]