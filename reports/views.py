from django.shortcuts import render
from users.decorators import seller_required
from products.models import Product
from orders.models import OrderItem
from .models import ShopVisit

@seller_required
def seller_report(request):
    shop = request.user.shop

    products_count = Product.objects.filter(shop=shop).count()

    orders_count = OrderItem.objects.filter(
        product__shop=shop
    ).values('order').distinct().count()

    visitors_count = ShopVisit.objects.filter(shop=shop).count()

    return render(request, 'reports/seller_report.html', {
        'products_count': products_count,
        'orders_count': orders_count,
        'visitors_count': visitors_count,
    })
