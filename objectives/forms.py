from django import forms
from .models import Objective

class ObjectiveForm(forms.ModelForm):
    class Meta:
        model = Objective
        fields = ['title', 'description', 'image']
        labels = {
            'title': 'Titlu',
            'description': 'Descriere',
            'image': 'Imagine',
        }