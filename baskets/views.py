from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Basket, BasketItem
from products.models import Product

@login_required
def view_basket(request):
    basket, created = Basket.objects.get_or_create(user=request.user)
    items = basket.items.all()
    return render(request, 'baskets/view_basket.html', {'basket': basket, 'items': items})


@login_required
def add_to_basket(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    basket, created = Basket.objects.get_or_create(user=request.user)
    
    existing_items = basket.items.select_related('product')
    if existing_items.exists():
        existing_seller = existing_items.first().product.shop.owner
        if product.shop.owner != existing_seller:
            return render(request, 'baskets/view_basket.html', {
                'basket': basket,
                'items': existing_items,
                'error_message': 'لا يمكنك إضافة منتجات من متجر مختلف في نفس السلة'
            })

    item, created = BasketItem.objects.get_or_create(basket=basket, product=product)
    if not created:
        item.quantity += 1
        item.save()

    return redirect(request.META.get('HTTP_REFERER', 'products:search_by_category'))




@login_required
def remove_from_basket(request, item_id):
    item = get_object_or_404(BasketItem, id=item_id)
    if item.basket.user != request.user:
        return redirect('baskets:view_basket')

    if request.method == 'POST':
        item.delete()
        return redirect('baskets:view_basket')

    return render(request, 'baskets/remove_from_basket.html', {'item': item})


@login_required
def clear_basket(request):
    basket = get_object_or_404(Basket, user=request.user)
    basket.items.all().delete()
    return redirect('baskets:view_basket')
