from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Bb, Profile


class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'content', 'rubric', 'price',)


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'about')
