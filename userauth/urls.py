from django.urls import path
from userauth import views

app_name = 'userauth'

urlpatterns = [
    # Authentication URLs
    path('sign-up/', views.signup_view, name='sign-up'),
    path('sign-in/', views.login_view, name='sign-in'),
    path('sign-out/', views.signout_view, name='sign-out'),
    
    # Password Reset URLs
    path('password-reset/', views.password_reset_request_view, name='password_reset'),
    path('password-reset/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),

    path('password-reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path('password-reset/complete/', views.password_reset_complete_view, name='password_reset_complete'),
]
