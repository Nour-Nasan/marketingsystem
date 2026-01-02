from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'productName', 'productPrice', 'category')
    list_filter = ('category',)
    search_fields = ('productName',)
    ordering = ('id',)

