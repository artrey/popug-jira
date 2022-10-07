from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

from apps.users.models import User


class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ["username", "role"]
