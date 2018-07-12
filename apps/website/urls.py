from django.urls import path
from . import views

app_name = 'apps.website'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('vlasom/', views.LandingView.as_view(), name='landing'),
]