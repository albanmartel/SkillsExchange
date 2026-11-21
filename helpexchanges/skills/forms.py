from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AdminUserCreationForm, UserCreationForm, UserChangeForm
from django.forms import ModelForm, TextInput, Textarea, formset_factory

from .models import Skill

NB_MAX_ACTIVITY = 10

# creation form for the admin in 'admin.py'
class CustomUserCreationFormAdmin(AdminUserCreationForm):
    """
    CustomUserCreationFormAdmin form
    Custom user creation form for the admin interface.
    """
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'bio',
            'is_staff',
            'is_active',
            'is_superuser',
        )

# modification form for the admin in 'admin.py'
class CustomUserChangeFormAdmin(UserChangeForm):
    """
    CustomUserChangeFormAdmin form
    Custom user modification form for the admin interface.
    """
    class Meta:
        model = get_user_model()
        fields = "__all__"

# creation form for public interface
class CustomUserCreationFormPublic(UserCreationForm):
    """
    CustomUserCreationFormAdmin form
    Custom user creation form for the admin interface.
    """
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'bio',
        )

# modification form for public interface
class CustomUserChangeFormPublic(forms.ModelForm):
    """
    CustomUserChangeFormAdmin form
    Custom user modification form for the admin interface.
    """
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'bio',
            'skills',
        )

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = [
            "skill_name",
            "skill_description",
        ]
        widgets = {
            "skill_name": TextInput(attrs={"size": 40}),
            "skill_description": Textarea(attrs={"cols": 80, "rows": 3}),
        }
