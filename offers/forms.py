from django import forms
from .models import OfferFlash
from products.models import Product

class OfferFlashForm(forms.ModelForm):
    class Meta:
        model = OfferFlash
        fields = ['product', 'old_price', 'new_price', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)

        if user and hasattr(user, 'shop'):
            self.fields['product'].queryset = Product.objects.filter(
                shop=user.shop
            )
        else:
            self.fields['product'].queryset = Product.objects.none()
