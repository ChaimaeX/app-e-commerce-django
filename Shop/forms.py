
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django import forms

from .models import *

from django.forms.widgets import PasswordInput, TextInput


# - Create/Register a user (Model Form)

class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']


# - Authenticate a user (Model Form)

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


def get_facture(pk):
    """ get invoice fonction """

    obj = Facture.objects.get(pk=pk)
    articles = CommandeProduct.objects.filter(facture=pk)
       

    context = {
        'obj': obj,
        'articles': articles
    }

    return context

