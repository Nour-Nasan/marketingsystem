from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['basket']  

        labels = {
            'basket': 'Required basket',
        }

        widgets = {
            'basket': forms.Select(attrs={'class': 'form-control'}),
        }


class OrderOptionsForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['contact_method', 'delivery_method']

        labels = {
            'contact_method': 'Select way to communicate',
            'delivery_method': 'Select delivery method',
        }

        widgets = {
            'contact_method': forms.RadioSelect(),
            'delivery_method': forms.RadioSelect(),
        }
