from django import forms
from django.contrib.auth import authenticate,get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from userauth.models import User

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _('The two password fields must match.'),
        'username_taken': _('A user with that username already exists.'),
        'email_taken': _('A user with that email address already exists.'),
        'required': _('This field is required.'),
        'invalid': _('Enter a valid value.'),
        'password_too_short': _('Your password must be at least 8 characters long.'),
        'password_common': _('Your password is too common.'),
        'password_strength': _('Password must contain both letters and numbers.'),
        'username_too_short': _('Username must be at least 4 characters long.'),
        'username_too_long': _('Username cannot exceed 150 characters.'),
        'username_invalid': _('Username must only contain letters and numbers.'),
        'email_format': _('Enter a valid email address.'),
        'email_invalid': _('Invalid email address.'),
        'password_no_special': _('Password must contain at least one special character.'),
    }

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': _('Username'),
            'email': _('Email Address'),
            'password1': _('Password'),
            'password2': _('Confirm Password'),
        }
        help_texts = {
            'username': _('Choose a unique username. Must be at least 4 characters long and only contain letters and '
                          'numbers.'),
            'email': _('Enter a valid email address. This will be used for account-related notifications.'),
            'password1': _('Your password must be at least 8 characters long and contain a mix of letters and numbers.'),
            'password2': _('Enter the same password as before, for verification.'),
        }

    def clean_username(self):
        username = self._extracted_from_clean_password1_2(
            'username', 4, 'username_too_short'
        )
        if len(username) > 150:
            raise ValidationError(self.error_messages['username_too_long'], code='username_too_long')
        if not username.isalnum():
            raise ValidationError(self.error_messages['username_invalid'], code='username_invalid')
        if User.objects.filter(username=username).exists():
            raise ValidationError(self.error_messages['username_taken'], code='username_taken')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError(self.error_messages['required'], code='required')
        try:
            forms.EmailField().clean(email)  # Validate email format
        except ValidationError as e:
            raise ValidationError(
                self.error_messages['email_format'], code='invalid'
            ) from e
        if User.objects.filter(email=email).exists():
            raise ValidationError(self.error_messages['email_taken'], code='email_taken')
        return email

    def clean_password1(self):
        password1 = self._extracted_from_clean_password1_2(
            'password1', 8, 'password_too_short'
        )
        if password1.lower() in ('password', '12345678', 'qwerty', 'abc123'):
            raise ValidationError(self.error_messages['password_common'], code='password_common')
        if password1.isdigit() or password1.isalpha():
            raise ValidationError(self.error_messages['password_strength'], code='password_strength')
        if all(
            char not in ' `~!@#$%^&*()-_=+[{]}|;:\'",<.>/?' for char in password1
        ):
            raise ValidationError(self.error_messages['password_no_special'], code='password_no_special')
        return password1

    # TODO Rename this here and in `clean_username` and `clean_password1`
    def _extracted_from_clean_password1_2(self, arg0, arg1, arg2):
        result = self.cleaned_data.get(arg0)
        if not result:
            raise ValidationError(self.error_messages['required'], code='required')
        if len(result) < arg1:
            raise ValidationError(self.error_messages[arg2], code=arg2)
        return result

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password2:
            raise ValidationError(self.error_messages['required'], code='required')
        if password1 and password1 != password2:
            raise ValidationError(self.error_messages['password_mismatch'], code='password_mismatch')
        return password2

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', self.error_messages['password_mismatch'])

        # Additional validation if needed
        if User.objects.filter(username=self.cleaned_data.get('username')).exists():
            self.add_error('username', self.error_messages['username_taken'])
        if User.objects.filter(email=self.cleaned_data.get('email')).exists():
            self.add_error('email', self.error_messages['email_taken'])




class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label=_("Email Address"),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        error_messages={
            'required': _('Email address is required.'),
            'invalid': _('Enter a valid email address.')
        },
        help_text=_('Enter the email address you used to register. Ensure it is correct and belongs to a registered '
                    'account.')
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        error_messages={
            'required': _('Password is required.'),
        },
        help_text=_('Enter your password to log in. Ensure it is correct and meets security requirements.')
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email:
            # Check if email format is valid
            try:
                forms.EmailField().clean(email)
            except ValidationError:
                self.add_error('email', _('Enter a valid email address.'))

            if not User.objects.filter(email=email).exists():
                self.add_error('email', _('No user with this email address exists. Please check the email or register '
                                          'if you are new.'))

        if password and email:
            user = authenticate(email=email, password=password)
            if user is None:
                self.add_error('password', _('Invalid password. Please check and try again.'))
            elif user and not user.is_active:
                self.add_error('email', _('This account is inactive. Please contact support for assistance.'))

        return cleaned_data

    def get_user(self):
        email = self.cleaned_data.get('email')
        return authenticate(email=email, password=self.cleaned_data.get('password'))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your registered email address'),
            'aria-describedby': 'emailHelp',
            'autofocus': True,
        }),
        help_text=_("Enter the email address associated with your account. We will send you an email with "
                    "instructions on how to reset your password."),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if not User.objects.filter(email=email).exists():
            raise ValidationError(_('No account found with this email address. Please check and try again.'))
        return email

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=None,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generates a one-use only link for resetting password and sends to the user.
        """
        email = self.cleaned_data["email"]
        users = User.objects.filter(email=email)
        for user in users:
            context = {
                'email': user.email,
                'domain': domain_override or request.get_host(),
                'site_name': _('Your Site Name'),
                'uid': user.pk,
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            context |= (extra_email_context or {})
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                user.email, html_email_template_name=html_email_template_name,
            )
            
            
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your new password'),
        }),
        help_text=_('Your new password must be at least 8 characters long, include both letters and numbers, and '
                    'contain at least one special character. It should not be a commonly used password.'),
    )
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Confirm your new password'),
        }),
        help_text=_('Re-enter your new password for confirmation.'),
    )

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        self.validate_password_strength(password1)
        return password1

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password1 != password2:
            raise ValidationError(_('The two password fields must match.'))
        return password2

    def validate_password_strength(self, password):
        if len(password) < 8:
            raise ValidationError(_('Your password must be at least 8 characters long.'))
        if password.lower() in ('password', '12345678', 'qwerty', 'abc123'):
            raise ValidationError(_('Your password is too common.'))
        if password.isdigit() or password.isalpha():
            raise ValidationError(_('Password must contain both letters and numbers.'))
        if all(
            char not in ' `~!@#$%^&*()-_=+[{]}|;:\'",<.>/?' for char in password
        ):
            raise ValidationError(_('Password must contain at least one special character.'))
