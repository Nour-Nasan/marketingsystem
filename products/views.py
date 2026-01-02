from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm 
from users.decorators import seller_required, buyer_required
from categories.models import Category
from .models import Product
from django.contrib import messages
from orders.models import OrderItem
from orders.models import OrderTracking 
from comments.views import buyer_can_comment 
from wishlist.models import WishlistItem


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    is_in_wishlist = False
    can_comment = False

    if request.user.is_authenticated:
        can_comment = buyer_can_comment(request.user, product)

        is_in_wishlist = WishlistItem.objects.filter(
            wishlist__user=request.user,
            product=product
        ).exists()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'can_comment': can_comment,
        'is_in_wishlist': is_in_wishlist,
    })


@buyer_required
def search_by_category(request):
    category_name = request.GET.get('category')
    sort = request.GET.get('sort')

    categories = Category.objects.values_list('name', flat=True).distinct()

    products = Product.objects.all()

    if category_name:
        products = products.filter(category__name__iexact=category_name.strip())

    if sort == 'price_asc':
        products = products.order_by('productPrice')
    elif sort == 'price_desc':
        products = products.order_by('-productPrice')

    wishlist_product_ids = set(
        WishlistItem.objects.filter(wishlist__user=request.user)
        .values_list('product_id', flat=True)
    )

    return render(request, 'products/search_by_category.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_name,
        'sort': sort,
        'wishlist_product_ids': wishlist_product_ids,
    })

@seller_required
def manage_products(request):
    products = Product.objects.filter(shop=request.user.shop)
    return render(request, 'products/manage_products.html', {'products': products})



@seller_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST or None, request.FILES or None, user=request.user)
        if form.is_valid():
            product = form.save(commit=False)
            product.shop = request.user.shop

            exists = Product.objects.filter(
                productName=product.productName,
                category=product.category,
                shop=product.shop
            ).exists()

            if exists:
                messages.error(request, "هذا المنتج موجود بالفعل ضمن نفس الفئة")
            else:
                product.save()
                return redirect('products:manage_products')
    else:
        form = ProductForm(user=request.user)

    return render(request, 'products/add_product.html', {'form': form})


@seller_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, shop=request.user.shop)

    if request.method == 'POST':
        form = ProductForm(request.POST or None, request.FILES or None, instance=product, user=request.user)
        if form.is_valid():
            updated_product = form.save(commit=False)

            exists = Product.objects.filter(
                productName=updated_product.productName,
                category=updated_product.category,
                shop=updated_product.shop
            ).exclude(id=product.id).exists()

            if exists:
                messages.error(request, "منتج آخر بنفس الاسم والفئة موجود بالفعل")
            else:
                updated_product.save()
                return redirect('products:manage_products')
    else:
        form = ProductForm(instance=product, user=request.user)

    return render(request, 'products/edit_product.html', {'form': form, 'product': product})


@seller_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, shop=request.user.shop)
    if request.method == 'POST':
        product.delete()
        return redirect('products:manage_products')
    return render(request, 'products/delete_product.html', {'product': product})


