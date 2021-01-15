from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Bb, Profile, Response, Reviews


class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'content', 'rubric', 'price',)

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'about', )


class ResponseForm(ModelForm):
    """Форма откликов"""
    class Meta:
        model = Response
        fields = ('text', )


class ReviewsForm(ModelForm):
    """Форма отзывов"""
    class Meta:
        model = Reviews
        fields = ('text', )