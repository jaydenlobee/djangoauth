# admin.py
from django.contrib import admin
from userauth.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_number', 'address', 'city', 'country', 'postal_code', 'date_of_birth', 'gender']
    search_fields = ['username', 'email']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    ordering = ['username']
    readonly_fields = ['date_joined', 'last_login']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'address', 'city', 'country', 'postal_code', 'profile_picture', 'date_of_birth', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)
