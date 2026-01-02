from django import forms
from .models import BasketItem

class BasketItemForm(forms.ModelForm):
    class Meta:
        model = BasketItem
        fields = ['quantity']
        labels = {
            'quantity': 'Quantity',
        }
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
        }
