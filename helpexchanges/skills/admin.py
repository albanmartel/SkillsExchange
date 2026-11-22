from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import AbstractUser
from wcwidth import width

from .forms import CustomUserCreationFormAdmin, CustomUserChangeFormAdmin
from .models import (
    Skill,
    Activity,
    Assistance,
    Appointment,
)

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
            'get_skills_display',
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
        ("Informations personnelles", {"fields": ("first_name", "last_name", "phone", "bio", "skills")}),
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("skills")

    @admin.display(description="Skills")
    def get_skills_display(self, obj):
        skill_names = [skill.skill_name for skill in obj.skills.all()]
        return ", ".join(skill_names) if skill_names else "-"

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

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("id_activity", "activity_title", "activity_description", "skill__skill_name")
    list_display_links = ("id_activity", "activity_title")
    search_fields = ("activity_title", "activity_description", "skill__skill_name")
    ordering = ("activity_title",)
    list_select_related = ("skill",)

@admin.register(Assistance)
class Assistance(admin.ModelAdmin):
    list_display = (
        "id_assistance",
        "author",
        "activity",
        "get_skill_name",
        "assistance_type",
        "assistance_status",
        "start_date_time",
        "end_date_time",
        "get_duration",
    )
    list_display_links = ("id_assistance", "author", "activity")
    search_fields = (
        "activity__activity_title",
        "activity__skill__skill_name",
        "author__username",
    )
    ordering = ("start_date_time",)
    list_select_related = ("author", "activity", "activity__skill")

    @admin.display(description="Skill Name", ordering="activity__skill__skill_name")
    def get_skill_name(self, obj):
        if obj.activity and obj.activity.skill:
            return obj.activity.skill.skill_name
        return "-"

    @admin.display(description="Duration")
    def get_duration(self, obj):
        duration = obj.get_duration()
        return duration if duration else "-"

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id_appointment_activity",
        "assistance",
        "get_author",
        "partner",
        "is_confirmed",
        "isConfirmedByOfferer",
        "confirmationDateTime",
    )
    list_display_links = (
        "id_appointment_activity",
        "assistance",
    )
    list_filter = (
        "is_confirmed",
        "isConfirmedByOfferer",
        "confirmationDateTime",
    )
    search_fields = (
        "assistance__activity__activity_title",
        "assistance__author__username",
        "partner__username",
        "partner__email",
    )
    ordering = ("-id_appointment_activity",)
    list_select_related = (
        "assistance",
        "assistance__author",
        "assistance__activity",
        "partner",
    )
    readonly_fields = ("confirmationDateTime",)
    actions = ("mark_as_confirmed",)

    fieldsets = (
        (
            "Participants & Assistance",
            {
                "fields": (
                    "assistance",
                    "partner",
                )
            },
        ),
        (
            "Confirmation",
            {
                "fields": (
                    "is_confirmed",
                    "isConfirmedByOfferer",
                    "confirmationDateTime",
                )
            },
        ),
    )

    @admin.display(description="Author", ordering="assistance__author__username")
    def get_author(self, obj):
        if obj.assistance and obj.assistance.author:
            return obj.assistance.author.username
        return "-"

    @admin.display(description="Activity title")
    def get_activity_title(self, obj):
        if obj.pk and obj.assistance and obj.assistance.activity:
            return obj.assistance.activity.activity_title
        return "-"

    @admin.action(description="Mark selected appointments as confirmed")
    def mark_as_confirmed(self, request, queryset):
        for appointment in queryset:
            appointment.set_confirmed()