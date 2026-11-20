from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'bio',
            'password',
            'is_staff',
            'is_active',
            'is_superuser',
            'last_login',
            'date_joined',
        ]

# Add this if the decorator isn’t working
admin.site.register(CustomUser, CustomUserAdmin)
