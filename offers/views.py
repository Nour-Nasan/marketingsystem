from django.shortcuts import render, redirect, get_object_or_404
from users.decorators import seller_required
from .models import OfferFlash
from .forms import OfferFlashForm
from django.utils import timezone
from products.models import Product

@seller_required
def add_offer(request):
    if request.method == 'POST':
        form = OfferFlashForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('offers:my_offers')
    else:
        form = OfferFlashForm(user=request.user)

    return render(request, 'offers/add_offer.html', {'form': form})

@seller_required
def my_offers(request):
    shop = request.user.shop 
    products = Product.objects.filter(shop=shop)
    offers = OfferFlash.objects.filter(product__in=products)

    return render(request, 'offers/my_offers.html', {'offers': offers})


@seller_required
def edit_offer(request, offer_id):
    offer = get_object_or_404(
        OfferFlash,
        id=offer_id,
        product__shop=request.user.shop
    )

    if request.method == 'POST':
        form = OfferFlashForm(request.POST, instance=offer, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('offers:my_offers')
    else:
        form = OfferFlashForm(instance=offer, user=request.user)

    return render(request, 'offers/edit_offer.html', {'form': form})

@seller_required
def delete_offer(request, offer_id):
    offer = get_object_or_404(
        OfferFlash,
        id=offer_id,
        product__shop=request.user.shop
    )

    if request.method == 'POST':
        offer.delete()
        return redirect('offers:my_offers')

    return render(request, 'offers/delete_offer.html', {
        'offer': offer
    })



def show_offers(request):
    now = timezone.now()

    offers = OfferFlash.objects.filter(
        is_active=True,
        start_date__lte=now,
        end_date__gte=now
    ).select_related('product')

    return render(request, 'offers/show_offers.html', {
        'offers': offers
    })
