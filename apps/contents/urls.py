from django.urls import path
from . import views

app_name = 'contents'
urlpatterns = [
    path('list/', views.ContentsList.as_view(), name = 'contents_list'),
    path('detail/<int:pk>/', views.ContentsDetail.as_view(), name = 'contents_detail'),
    path('create/', views.ContentsCreate.as_view(), name = 'contents_create'),
    path('update/<int:pk>/', views.ContentsUpdate.as_view(), name = 'contents_update'),
]