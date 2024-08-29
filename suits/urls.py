from django.urls import path
from . import views

app_name = 'suits'  # Define the app namespace

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('dashboard/', views.dashboard_page, name='dashboard_page'),
    path('dashboardo/', views.dashboardo_page, name='dashboardo_page'),
    path('matters/', views.matters_page, name='matters_page'),
    path('calendar/', views.calendar_page, name='calendar_page'),
    path('tasks-projects/', views.tasks_projects_page, name='tasks_projects_page'),
    path('contacts/', views.contacts_page, name='contacts_page'),
    path('documents/', views.documents_page, name='documents_page'),
    path('billing-time-tracking/', views.billing_time_tracking_page, name='billing_time_tracking_page'),
    path('reporting/', views.reporting_page, name='reporting_page'),
    path('internal-communication/', views.internal_communication_page, name='internal_communication_page'),
    path('settings/', views.settings_page, name='settings_page'),
    path('nc/', views.dashboard_page, name='nc_page'),  # Map /nc/ to dashboard_page view
]
