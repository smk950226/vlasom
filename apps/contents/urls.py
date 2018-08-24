from django.urls import path
from . import views

app_name = 'contents'
urlpatterns = [
    path('list/<int:category_id>/', views.ContentsList.as_view(), name = 'contents_list'),
    path('hot/list/', views.ContentsList.as_view(), name = 'contents_list_hot'),
    path('new/list/', views.ContentsList.as_view(), name = 'contents_list_new'),
    path('detail/<int:pk>/', views.ContentsDetail.as_view(), name = 'contents_detail'),
    path('create/', views.ContentsCreate.as_view(), name = 'contents_create'),
    path('update/<int:pk>/', views.ContentsUpdate.as_view(), name = 'contents_update'),
    path('delete/<int:pk>/', views.contents_delete, name = 'contents_delete'),
    path('uploaded/', views.ContentsList.as_view(), name = 'contents_list_uploaded'),
]