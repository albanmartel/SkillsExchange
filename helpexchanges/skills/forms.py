from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AdminUserCreationForm, UserCreationForm, UserChangeForm


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

