from django import forms
from .models import Shop
from users.models import CustomUser


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['owner','shopName', 'shopDescription', 'shopAddress', 'shopNumber', 'shopEmail'] 
        
        labels = { 
            'shopName': 'Name',
            'shopDescription': 'Description',
            'shopAddress': 'Address',
            'shopNumber': 'Phone number',
            'shopEmail': 'Email',
        }

        widgets = {
            'shopName': forms.TextInput(attrs={'class': 'form-control'}),
            'shopDescription': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'shopAddress': forms.TextInput(attrs={'class': 'form-control'}),
            'shopNumber': forms.TextInput(attrs={'class': 'form-control'}),
            'shopEmail': forms.EmailInput(attrs={'class': 'form-control'}),
        }



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # عرض فقط المستخدمين البائعين
        self.fields['owner'].queryset = CustomUser.objects.filter(role='seller')




class SellerShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['shopName', 'shopDescription', 'shopAddress', 'shopNumber', 'shopEmail']
        
        labels = {
            'shopName': 'Name',
            'shopDescription': 'Description',
            'shopAddress': 'Address',
            'shopNumber': 'Phone number',
            'shopEmail': 'Email',
        }

        widgets = {
            'shopName': forms.TextInput(attrs={'class': 'form-control'}),
            'shopDescription': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'shopAddress': forms.TextInput(attrs={'class': 'form-control'}),
            'shopNumber': forms.TextInput(attrs={'class': 'form-control'}),
            'shopEmail': forms.EmailInput(attrs={'class': 'form-control'}),
        }
