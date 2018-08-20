from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/',auth_views.logout, name='logout', kwargs = {'next_page': '/',}),
    path('profile/',views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.UserUpdate.as_view(), name='user_update'),
    path('verify/', views.UserVerify.as_view(), name='user_verify'),
    path('signup/', views.UserCreate.as_view(), name='user_create'),
    path('signup/confirm/<uidb64>/<token>/', views.UserConfirm.as_view(), name='user_confirm'),

    path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),

    path('find/id/', views.FindId.as_view(), name = 'find_id'),
]
