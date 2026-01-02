from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'basket', 'status')
    list_filter = ('status',)
    search_fields = ('buyer__username', 'basket__id')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product')
    search_fields = ('order__id', 'product__id')
