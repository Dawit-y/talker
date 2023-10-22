from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Post


class UserRegistrationForm(UserCreationForm):
   class Meta:
        model = User
        fields = ['username', 'email' , 'password1', 'password2']
        help_texts = {
            'username': None,
            'password': None,
            'password2': None,
        }

class PostForm(forms.ModelForm): 
    class Meta:
        model = Post
        fields = ("image", "content")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = False    
