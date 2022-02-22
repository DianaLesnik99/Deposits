from django import forms
from django.contrib.auth.models import User

from .models import *


class SubsoilUsersForm(forms.Form):
    subsoil_users = forms.ModelChoiceField(queryset=SubsoilUsers.objects.all(),
                                           empty_label="---Выберите недропользователя---",
                                           label='Недропользователь')
