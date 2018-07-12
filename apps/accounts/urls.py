from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/',auth_views.logout, name='logout', kwargs = {'next_page': '/',}),
    path('profile/',views.profile, name='profile'),
    path('profile/update/', views.UserUpdate.as_view(), name='user_update'),
    path('verify/', views.UserVerify.as_view(), name='user_verify'),
    path('signup/', views.UserCreate.as_view(), name='user_create'),
    path('signup/confirm/<uidb64>/<token>/', views.UserConfirm.as_view(), name='user_confirm'),

    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
]
