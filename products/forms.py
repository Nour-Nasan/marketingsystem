from django import forms
from .models import Product
from categories.models import Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['productName','productDescription','productPrice','productImage','category',]

        labels = {
            'productName': 'Product name',
            'productPrice': 'Price',
            'productImage': 'Img',
            'category': 'category',
            'productDescription':'Description'
        }
        
        widgets = {
            'productName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'productPrice': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'productImage': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'productDescription': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Enter product description','rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(seller=user)
