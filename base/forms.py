# Custom file created manually
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User
# from django.contrib.auth.models import User
from django.forms import ImageField, FileInput

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    
    avatar = ImageField(widget=FileInput)
    class Meta:
        model = User
        fields = ['avatar','name', 'username', 'email', 'bio']

