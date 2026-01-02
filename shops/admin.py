from django.contrib import admin
from .models import Shop

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('shopName', 'shopAddress', 'shopNumber', 'shopEmail')  
    search_fields = ('shopName', 'shopAddress', 'shopEmail')  
    list_filter = ('shopName', 'shopAddress')  
    ordering = ('shopName',)  


