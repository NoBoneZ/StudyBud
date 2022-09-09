from django import forms
from.models import Room, User
from django.contrib.auth.forms import UserCreationForm


class MyUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name","email", "bio", "avatar", "password1", "password2"]


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ["host", "participants"]
        

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "bio","avatar","username", "email"]