from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput
        (
        attrs={
            'class': 'form-control',
            'placeholder': 'Имя'
        }
    ), label='', required=True)
    last_name = forms.CharField(widget=forms.TextInput
        (
        attrs={
            'class': 'form-control',
            'placeholder': 'Фамилия'
        }
    ), label='', required=True)
    email = forms.EmailField(widget=forms.TextInput
        (
        attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        }
    ), label='', required=True)
    phone = forms.CharField(widget=forms.TextInput
        (
        attrs={
            'class': 'form-control',
            'placeholder': 'Телефон'
        }
    ), label='', required=True)

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'email', 'phone')
