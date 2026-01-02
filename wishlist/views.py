from django.shortcuts import render, redirect, get_object_or_404
from users.decorators import buyer_required
from .models import Wishlist, WishlistItem
from products.models import Product


@buyer_required
def view_wishlist(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    items = wishlist.items.select_related('product').all()
    return render(request, 'wishlist/view_wishlist.html', {'items': items})


@buyer_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

    item = WishlistItem.objects.filter(wishlist=wishlist, product=product).first()
    if item:
        item.delete()
    else:
        WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)

    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or 'wishlist:view_wishlist'
    return redirect(next_url)


@buyer_required
def remove_item(request, item_id):
    item = get_object_or_404(WishlistItem, id=item_id, wishlist__user=request.user)
    item.delete()
    return redirect('wishlist:view_wishlist')
