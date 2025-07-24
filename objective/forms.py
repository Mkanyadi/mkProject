from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nume utilizator',
            'email': 'Email',
            'password1': 'Parolă',
            'password2': 'Confirmă parolă',
        }

    def __init__(self, *args, **kwargs):
            super(UserRegisterForm, self).__init__(*args, **kwargs)
            self.fields['username'].widget.attrs['placeholder'] = 'Nume utilizator'
            self.fields['email'].widget.attrs['placeholder'] = 'exemplu@email.com'
            self.fields['password1'].widget.attrs['placeholder'] = 'Introduceți o parolă sigură'
            self.fields['password2'].widget.attrs['placeholder'] = 'Reintroduceți parola'