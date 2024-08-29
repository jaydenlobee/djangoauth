from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static


# Create your views here.

def landing_page(request):
    return render(request, 'dashboard/landing.html')


@login_required(login_url='userauth:sign-in')
def dashboard_page(request):
    # Define the WebSocket URL for local development
    websocket_url = f"ws://localhost:8000/cable?jid={request.user.id}"  # Example dynamic value, adjust as needed

    context = {
        'layout': 'default',
        'nav_items': [
            {'label': 'Dashboard', 'icon': 'fa-tachometer-alt'},
            {'label': 'Matters', 'icon': 'fa-briefcase'},
            {'label': 'Calendar', 'icon': 'fa-calendar-alt'},
            {'label': 'Tasks', 'icon': 'fa-tasks'},
            {'label': 'Documents', 'icon': 'fa-file-alt'},
            {'label': 'Contacts', 'icon': 'fa-address-book'},
            {'label': 'Billing', 'icon': 'fa-file-invoice-dollar'},
            {'label': 'Time Tracking', 'icon': 'fa-clock'},
            {'label': 'Reporting', 'icon': 'fa-chart-bar'},
            {'label': 'Internal Communication', 'icon': 'fa-comments'},
            {'label': 'Settings', 'icon': 'fa-cogs'},
            # Add more nav items as needed
        ],
        'is_banner_visible': True,
        'display_exp846': True,
        'show_impersonation_banner': True,
        'show_trust_reconciliation_banner': True,
        'show_disabled_email_banner': True,
        'show_trial_banner': False,
        'show_practice_area_banner': True,
        'notifications': [
            {'message': 'New matter assigned', 'type': 'info'},
            {'message': 'Invoice #1234 overdue', 'type': 'warning'},
            {'message': 'Task deadline approaching', 'type': 'alert'},
            # Add more notifications as needed
        ],
        'recents': [
            {'label': 'Matter XYZ', 'url': '#'},
            {'label': 'Client ABC', 'url': '#'},
            # Add more recents as needed
        ],
        'search_placeholder': 'Search for matters, contacts, documents...',
        'user_profile': {
            'name': request.user.get_full_name(),
            'email': request.user.email,
            # 'profile_pic_url': static('images/suits.jpg'),  # Use static template tag for proper path
        },
        'websocket_url': websocket_url,  # Pass the WebSocket URL to the context
    }
    return render(request, 'dashboard/dashboard.html', context)


def dashboardo_page(request):
    return render(request, 'client/dashboardo.html')


def matters_page(request):
    return render(request, 'client/matters.html')


def calendar_page(request):
    return render(request, 'client/calendar.html')


def tasks_projects_page(request):
    return render(request, 'client/tasks_projects.html')


def contacts_page(request):
    return render(request, 'client/contacts.html')


def documents_page(request):
    return render(request, 'client/documents.html')


def billing_time_tracking_page(request):
    return render(request, 'client/billing_time_tracking.html')


def reporting_page(request):
    return render(request, 'client/reporting.html')


def internal_communication_page(request):
    return render(request, 'client/internal_communication.html')


def settings_page(request):
    return render(request, 'client/settings.html')


@login_required(login_url='userauth:sign-in')
def nc_page(request):
    return HttpResponse("This is a placeholder for /nc/")
