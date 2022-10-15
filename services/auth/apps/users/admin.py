from django.contrib import admin
from django.contrib.auth import admin as base_admin
from django.utils.translation import gettext_lazy as _

from apps.users.forms import UserCreationForm
from apps.users.models import User


@admin.register(User)
class UserAdmin(base_admin.UserAdmin):
    add_form = UserCreationForm
    list_display = [
        "public_id",
        "username",
        "first_name",
        "last_name",
        "role",
        "last_login",
        "date_joined",
        "is_staff",
    ]
    list_filter = ["is_staff", "is_superuser", "is_active", "role"]
    readonly_fields = ["last_login", "date_joined"]
    list_editable = ["role"]
    search_fields = ["username", "first_name", "last_name", "email", "public_id"]
    fieldsets = (
        (None, {"fields": ("public_id", "username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "role"),
            },
        ),
    )
