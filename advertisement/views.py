from django.shortcuts import render, redirect, get_object_or_404
from users.decorators import seller_required
from .models import Advertisement
from .forms import AdvertisementForm


@seller_required
def my_ads(request):
    ads = Advertisement.objects.filter(seller=request.user)
    return render(request, 'advertisement/my_ads.html', {
        'ads': ads
    })


@seller_required
def add_advertisement(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.seller = request.user
            ad.save()
            return redirect('advertisement:my_ads')
    else:
        form = AdvertisementForm()

    return render(request, 'advertisement/add_ad.html', {'form': form})


@seller_required
def edit_advertisement(request, ad_id):
    ad = get_object_or_404(Advertisement, id=ad_id, seller=request.user)

    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('advertisement:my_ads')
    else:
        form = AdvertisementForm(instance=ad)

    return render(request, 'advertisement/edit_ad.html', {'form': form})


@seller_required
def delete_advertisement(request, ad_id):
    ad = get_object_or_404(Advertisement, id=ad_id, seller=request.user)

    if request.method == 'POST':
        ad.delete()
        return redirect('advertisement:my_ads')

    return render(request, 'advertisement/delete_ad.html', {
        'ad': ad
    })


def show_advertisements(request):
    ads = Advertisement.objects.all()
    return render(request, 'advertisement/show_ads.html', {'ads': ads})
