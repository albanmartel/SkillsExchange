from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
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
    )
    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name",
        "phone"
    )
    ordering = (
        'username',
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Informations personnelles", {"fields": ("first_name", "last_name", "phone", "bio")}),
        (
            "Permissions et rôles",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Dates importantes", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "phone",
                    "bio",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

# Add this if the decorator isn’t working
admin.site.register(CustomUser, CustomUserAdmin)
