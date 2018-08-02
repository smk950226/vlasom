from django.urls import path
from . import views

app_name = 'preference'
urlpatterns = [
    path('like/<int:pk>/', views.like_create, name = 'like_create'),
    path('interest/contents/<int:pk>/', views.interest_create_contents, name = 'interest_create_contents'),
    path('interest/category/<int:pk>/', views.interest_create_category, name = 'interest_create_category'),
    path('interest/list/', views.InterestContentsList.as_view(), name = 'interest_list'),
]