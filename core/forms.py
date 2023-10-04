from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
   class Meta:
        model = User
        fields = ['username', 'email' , 'password1', 'password2']
        help_texts = {
            'username': None,
            'password': None,
            'password2': None,
        }