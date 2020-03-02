from django import forms
from .models import Client, Order


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
    email = forms.EmailField(widget=forms.EmailInput
        (
        attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        }
    ), label='', required=True)
    phone = forms.CharField(widget=forms.NumberInput
        (
        attrs={
            'class': 'form-control',
            'placeholder': 'Телефон',
            'type': 'tel',
            'inputmode': 'tel',
            'minlength': '11',
            'maxlength': '12',
            'pattern': '^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
        }
    ), label='', required=True)

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'email', 'phone')


class OrderForm(forms.ModelForm):
    addition = forms.CharField(widget=forms.Textarea
        (
        attrs={
            'class': 'form-control',
            'placeholder': 'Комментарий к заказу',
            'type': 'text',
            'maxlength': '600',
            'style': 'height: 150px;',
        }
    ), label='', required=False)

    class Meta:
        model = Order
        fields = ('addition',)
