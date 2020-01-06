from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput
        (
        attrs={
            'class': 'form-control',
            'placeholder': 'Имя'
        }
    ), label='')
    last_name = forms.CharField(widget=forms.TextInput
        (
        attrs={
            'class': 'form-control',
            'placeholder': 'Фамилия'
        }
    ), label='')
    email = forms.CharField(widget=forms.TextInput
        (
        attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        }
    ), label='')
    phone = forms.CharField(widget=forms.TextInput
        (
        attrs={
            'class': 'form-control',
            'placeholder': 'Телефон'
        }
    ), label='')

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'email', 'phone')
