from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.middleware.csrf import get_token
import logging
from django.http import JsonResponse

from userauth.forms import CustomPasswordResetForm, CustomSetPasswordForm, UserLoginForm, UserRegisterForm

logger = logging.getLogger(__name__)

# Helper functions
def handle_ajax_request(success, message, errors=None, redirect_url=None):
    response = {
        'success': success,
        'message': message,
        'errors': errors,
        'redirect_url': redirect_url
    }
    return JsonResponse(response)

def handle_form_errors(request, form, error_message=None, template_name=None):
    if error_message:
        form.add_error(None, error_message)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return handle_ajax_request(False, error_message, errors=form.errors)
    return render(request, template_name, {'form': form, 'csrf_token': get_token(request)})

# Password Reset Request View
@csrf_protect
def password_reset_request_view(request):
    # sourcery skip: remove-unnecessary-else, swap-if-else-branches
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_user_model().objects.filter(email=email).first()
            if user:
                try:
                    send_password_reset_email(request, user)
                    message = _("We've emailed you instructions for resetting your password. Please check your inbox.")
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return handle_ajax_request(True, message, redirect_url=reverse('userauth:password_reset_done'))
                    messages.success(request, message)
                    return redirect('userauth:password_reset_done')
                except Exception as e:
                    logger.error(f"Error sending password reset email: {e}")
                    message = _("There was an error sending the password reset email. Please try again later.")
                    return handle_form_errors(request, form, error_message=message, template_name='userauth/password_reset_form.html')
            else:
                message = _("No account found with this email address.")
                return handle_form_errors(request, form, error_message=message, template_name='userauth/password_reset_form.html')
        else:
            return handle_form_errors(request, form, template_name='userauth/password_reset_form.html')
    else:
        form = CustomPasswordResetForm()

    context = {
        "form": form,
        "csrf_token": get_token(request)
    }
    return render(request, 'userauth/password_reset_form.html', context)

# Send Password Reset Email
def send_password_reset_email(request, user):
    token_generator = default_token_generator
    subject = _("Password Reset Requested")
    email_template_name = "userauth/password_reset_email.html"
    context = {
        'email': user.email,
        'domain': request.get_host(),
        'site_name': _('Your Site Name'),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        'token': token_generator.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    }
    email_content = render_to_string(email_template_name, context)
    send_mail(
        subject,
        email_content,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
        html_message=email_content
    )
    logger.info(f"Password reset email sent to {user.email}")

# Password Reset Confirm View
@csrf_protect
def password_reset_confirm_view(request, uidb64=None, token=None):
    # sourcery skip: remove-unnecessary-else, swap-if-else-branches
    if uidb64 is None or token is None:
        message = _("The password reset link is invalid. Please request a new one.")
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return handle_ajax_request(False, message, redirect_url=reverse('userauth:password_reset'))
        messages.error(request, message)
        return redirect('userauth:password_reset')

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    token_generator = default_token_generator

    if user is not None and token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                message = _("Your password has been reset successfully. You can now log in with your new password.")
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return handle_ajax_request(True, message, redirect_url=reverse('userauth:sign-in'))
                messages.success(request, message)
                return redirect('userauth:sign-in')
            else:
                return handle_form_errors(request, form, template_name='userauth/password_reset_confirm.html')
        else:
            form = CustomSetPasswordForm(user)

        context = {
            'form': form,
            'csrf_token': get_token(request),
            'uid': uidb64,
            'token': token
        }
        return render(request, 'userauth/password_reset_confirm.html', context)
    else:
        message = _("The password reset link is invalid or has expired. Please request a new one.")
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return handle_ajax_request(False, message, redirect_url=reverse('userauth:password_reset'))
        messages.error(request, message)
        return redirect('userauth:password_reset')


# Password Reset Done View
def password_reset_done_view(request):
    message = _("If an account exists with the email you entered, you should receive password reset instructions shortly.")
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return handle_ajax_request(True, message, redirect_url=reverse('userauth:sign-in'))
    messages.info(request, message)
    return render(request, 'userauth/password_reset_done.html')

# Password Reset Complete View
def password_reset_complete_view(request):
    message = _("Your password has been reset successfully.")
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return handle_ajax_request(True, message, redirect_url=reverse('userauth:sign-in'))
    messages.success(request, message)
    return render(request, 'userauth/password_reset_complete.html')

@csrf_protect
def signup_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if not form.is_valid():
            return handle_form_errors(request, form)
        new_user = form.save()
        user = authenticate(email=form.cleaned_data.get('email'), password=form.cleaned_data.get('password1'))
        if user is not None:
            return handle_successful_signup(request, user, form)
        message = "Account creation was successful, but we could not automatically log you in."
        return handle_form_errors(request, form, message)
    else:
        form = UserRegisterForm()

    context = {
        "form": form,
        "csrf_token": get_token(request)
    }
    return render(request, "userauth/sign-up.html", context)

def handle_successful_signup(request, user, form):
    login(request, user)
    username = form.cleaned_data.get("username")
    message = (f"Hey {username}, your account was created successfully. You have been logged in and redirected to your "
               f"dashboard.")

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return handle_ajax_request(True, message, redirect_url=reverse('suits:dashboard_page'))
    messages.success(request, message)
    return redirect('suits:dashboard_page')

@csrf_protect
def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if not form.is_valid():
            return handle_form_errors(request, form)
        user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        if user is None:
            return handle_form_errors(request, form, "Invalid email or password.")
        login(request, user)
        message = f"Welcome back, {user.username}! You have successfully logged in."
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return handle_ajax_request(True, message, redirect_url=reverse('suits:dashboard_page'))
        messages.success(request, message)
        return redirect('suits:dashboard_page')
    else:
        form = UserLoginForm()

    context = {
        "form": form,
        "csrf_token": get_token(request)
    }
    return render(request, "userauth/sign-in.html", context)

@csrf_exempt
def signout_view(request):
    if request.method == "POST":
        logout(request)
        message = "You have been successfully logged out."
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': message, 'redirect_url': reverse('userauth:sign-in')})
        messages.success(request, message)
        return redirect('userauth:sign-in')
    else:
        context = {
            "csrf_token": get_token(request)
        }
        return render(request, "userauth/sign-out.html", context)