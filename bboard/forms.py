from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Bb


class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'content', 'rubric', 'price', )

