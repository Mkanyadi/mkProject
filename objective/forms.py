from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Objective

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

class ObjectiveMemoryForm(forms.ModelForm):
    class Meta:
        model = Objective
        fields = [
            'title',
            'description',
            'image',
            'memory_date',
            'memory_location',
            'memory_with',
            'memory_repeat',
            'memory_rating',
            'memory_thoughts',
        ]
        widgets = {
            'memory_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'memory_location': forms.TextInput(attrs={'class': 'form-control'}),
            'memory_with': forms.TextInput(attrs={'class': 'form-control'}),
            'memory_repeat': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'memory_rating': forms.NumberInput(attrs={'min': 1, 'max': 10, 'class': 'form-range'}),
            'memory_thoughts': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'memory_date': 'Data',
            'memory_location': 'Locația',
            'memory_with': 'Cu cine',
            'memory_repeat': 'Ai repeta experiența?',
            'memory_rating': 'Evaluare (1–10)',
            'memory_thoughts': 'Gânduri și amintiri',
            'image': 'Adaugă o imagine',
        }
