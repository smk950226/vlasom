from django.urls import path
from . import views

app_name = 'apps.website'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('vlasom/', views.LandingView.as_view(), name='landing'),
    path('search/', views.SearchResult.as_view(), name='search'),
    path('terms/access/', views.TermView.as_view(), name='term_access'),
    path('terms/information/', views.TermView.as_view(), name='term_information'),
]