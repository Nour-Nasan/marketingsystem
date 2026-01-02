from django.shortcuts import render, redirect, get_object_or_404
from .models import Shop
from .forms import SellerShopForm
from users.decorators import seller_required
from shops.models import Shop
from products.models import Product
from django.shortcuts import render, get_object_or_404
from reports.models import ShopVisit
from products.models import Product

# =========================
# Buyer Views
# =========================

def shop_list(request):
    shops = Shop.objects.all()
    return render(request, 'shops/shop_list.html', {'shops': shops})


def shop_detail(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    products = Product.objects.filter(shop=shop)
    ShopVisit.objects.create(shop=shop)
    return render(request, 'shops/shop_detail.html', {
        'shop': shop,
        'products': products
    })


# =========================
# Seller Views
# =========================


@seller_required
def manage_shop(request):
    try:
        shop = request.user.shop  
    except Shop.DoesNotExist:
        return redirect('shops:add_shop')  

    return render(request, 'shops/manage_shop.html', {'shop': shop})


@seller_required
def add_shop(request):
    if hasattr(request.user, 'shop'):
        return redirect('shops:manage_shop')

    if request.method == 'POST':
        form = SellerShopForm(request.POST)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.owner = request.user
            shop.save()
            return redirect('shops:manage_shop')
    else:
        form = SellerShopForm()
    return render(request, 'shops/add_shop.html', {'form': form})


@seller_required
def edit_shop(request):
    shop = get_object_or_404(Shop, owner=request.user)
    if request.method == 'POST':
        form = SellerShopForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            return redirect('shops:manage_shop')
    else:
        form = SellerShopForm(instance=shop)
    return render(request, 'shops/edit_shop.html', {'form': form, 'shop': shop})


@seller_required
def delete_shop(request, shop_id):
    shop = get_object_or_404(Shop, owner=request.user, id=shop_id)
    if request.method == 'POST':
        shop.delete()
        return redirect('shops:add_shop')
    return render(request, 'shops/delete_shop.html', {'shop': shop})

