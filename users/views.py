from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .decorators import admin_required, buyer_required, seller_required
from .forms import RegisterForm, ProfileUpdateForm
from shops.models import Shop
from shops.forms import ShopForm
from django.utils import timezone
from offers.models import OfferFlash
from advertisement.models import Advertisement

# ------------------ Public Views ------------------

def home(request):
    return render(request, 'users/home.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('users:redirect_after_login')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('users:login')


# ------------------ Account profile ------------------

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث بيانات الحساب.')
            return redirect('users:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})


# ------------------ Redirect After Login ------------------

@login_required
def redirect_after_login(request):
    if request.user.is_admin():
        return redirect('users:admin_dashboard')
    elif request.user.is_buyer():
        return redirect('users:buyer_dashboard')
    elif request.user.is_seller():
        return redirect('users:seller_dashboard')
    else:
        return redirect('users:login')


# ------------------ Dashboards ------------------

@admin_required
def admin_dashboard(request):
    shops = Shop.objects.all()
    return render(request, 'users/admin_dashboard.html', {'shops': shops})


@buyer_required
def buyer_dashboard(request):
    return render(request, 'users/buyer_dashboard.html')


@seller_required
def seller_dashboard(request):
    return render(request, 'users/seller_dashboard.html')


# ------------------ Admin Shop Management ------------------

@admin_required
def add_shop_admin(request):
    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:admin_dashboard')
    else:
        form = ShopForm()

    return render(request, 'users/add_shop_admin.html', {'form': form})


@admin_required
def delete_shop_admin(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    if request.method == 'POST':
        shop.delete()
        return redirect('users:admin_dashboard')

    return render(request, 'users/delete_shop_admin.html', {'shop': shop})


# ------------------ Errors ------------------

def error_403(request):
    return render(request, 'users/error_403.html', status=403)



# ------------------ Buyer advertisement & flash offers ------------------

@buyer_required
def buyer_dashboard(request):
    ads = Advertisement.objects.all()

    offers = OfferFlash.objects.filter(
        is_active=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).select_related('product')

    return render(request, 'users/buyer_dashboard.html', {
        'ads': ads,
        'offers': offers
    })
