from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationFormAdmin, CustomUserChangeFormAdmin
from .models import Skill

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    """
    CustomUserAdmin
    This class allows you to customise the forms
    that will be used in the administrator interface
    """
    add_form = CustomUserCreationFormAdmin
    form = CustomUserChangeFormAdmin
    model = CustomUser
    # Columns displayed in the user changelist view
    list_display = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'bio',
            'is_staff',
            'is_active',
            'is_superuser',
            'last_login',
            'date_joined',
    )

    # Fields searched by the admin search bar
    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name",
        "phone"
    )

    # Default sort order in the admin user list
    ordering = (
        'username',
    )

    # Use a dual-list widget for many-to-many group and permission assignments
    filter_horizontal = (
        "groups",
        "user_permissions",
        "skills",
    )

    # Field sections on the existing user edit page
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

    # Fields displayed when creating a new user from the admin
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": tuple(
                    dict.fromkeys(
                        (
                            *UserAdmin.add_fieldsets[0][1]["fields"],
                            "email",
                            "first_name",
                            "last_name",
                            "phone",
                            "bio",
                            "is_staff",
                            "is_active",
                            "is_superuser",
                        )
                    )
                ),
            },
        ),
    )

# Add this if the decorator isn’t working
admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """
    Allows you to create, list, search for and edit skills in /admin/
    """
    # Columns displayed in the list table
    list_display = ("id_skill", "skill_name", "skill_description")

    # Add a link to the skill name to edit it
    list_display_links = ("id_skill", "skill_name")

    # Search bar at the top of the list
    search_fields = ("skill_name", "skill_description")

    # Default alphabetical sort
    ordering = ("skill_name",)