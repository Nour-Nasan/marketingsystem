from django.contrib import messages
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from notifications.models import Notification
from users.decorators import bazar_organizer_required, seller_required

from .forms import BazaarForm
from .models import Bazaar, BazaarBooking


@bazar_organizer_required
def my_bazaars(request):
    bazaars = Bazaar.objects.filter(organizer=request.user).order_by('-start_datetime')
    return render(request, 'bazaar/my_bazaars.html', {'bazaars': bazaars})


@bazar_organizer_required
def add_bazaar(request):
    if request.method == 'POST':
        form = BazaarForm(request.POST, request.FILES)
        if form.is_valid():
            bazaar = form.save(commit=False)
            bazaar.organizer = request.user
            bazaar.save()
            return redirect('bazaar:my_bazaars')
    else:
        form = BazaarForm()
    return render(request, 'bazaar/bazaar_form.html', {'form': form, 'is_edit': False})


@bazar_organizer_required
def edit_bazaar(request, bazaar_id):
    bazaar = get_object_or_404(Bazaar, pk=bazaar_id, organizer=request.user)
    if request.method == 'POST':
        form = BazaarForm(request.POST, request.FILES, instance=bazaar)
        if form.is_valid():
            form.save()
            return redirect('bazaar:my_bazaars')
    else:
        form = BazaarForm(instance=bazaar)
    return render(
        request,
        'bazaar/bazaar_form.html',
        {'form': form, 'is_edit': True, 'bazaar': bazaar},
    )


@bazar_organizer_required
def delete_bazaar(request, bazaar_id):
    bazaar = get_object_or_404(Bazaar, pk=bazaar_id, organizer=request.user)
    if request.method == 'POST':
        bazaar.delete()
        return redirect('bazaar:my_bazaars')
    return render(request, 'bazaar/delete_bazaar.html', {'bazaar': bazaar})


@seller_required
def browse_bazaars(request):
    bazaars = Bazaar.objects.all().order_by('start_datetime')
    return render(request, 'bazaar/browse_bazaars.html', {'bazaars': bazaars})


@seller_required
def bazaar_detail(request, bazaar_id):
    bazaar = get_object_or_404(Bazaar, pk=bazaar_id)
    return render(
        request,
        'bazaar/bazaar_detail.html',
        {
            'bazaar': bazaar,
        },
    )


@seller_required
def request_booking(request, bazaar_id):
    messages.info(request, 'Please confirm your booking before submitting.')
    return redirect('bazaar:confirm_booking', bazaar_id=bazaar_id)


@seller_required
def confirm_booking(request, bazaar_id):
    bazaar = get_object_or_404(Bazaar, pk=bazaar_id)
    existing_booking = BazaarBooking.objects.filter(seller=request.user, bazaar=bazaar).first()

    if request.method == 'POST':
        if existing_booking:
            messages.info(request, 'You already have a booking request for this bazaar.')
            return redirect('bazaar:my_bookings')

        try:
            with transaction.atomic():
                booking = BazaarBooking.objects.create(
                    seller=request.user,
                    bazaar=bazaar,
                    status='pending',
                )
                Notification.objects.create(
                    recipient=bazaar.organizer,
                    sender=request.user,
                    title='New Bazaar Booking Request',
                    message=f'{request.user.username} requested booking for bazaar "{bazaar.title}".',
                    notification_type='bazaar_booking_request',
                    url=reverse('bazaar:organizer_bookings'),
                )
        except IntegrityError:
            messages.info(request, 'You already have a booking request for this bazaar.')
            return redirect('bazaar:my_bookings')

        messages.success(request, 'Booking request submitted (Pending).')
        return redirect('bazaar:my_bookings')

    return render(
        request,
        'bazaar/confirm_booking.html',
        {
            'bazaar': bazaar,
            'existing_booking': existing_booking,
        },
    )


@seller_required
def my_bookings(request):
    bookings = (
        BazaarBooking.objects.filter(seller=request.user)
        .select_related('bazaar', 'bazaar__organizer')
        .order_by('-created_at')
    )
    return render(
        request,
        'bazaar/my_bookings.html',
        {
            'bookings': bookings,
            'now': timezone.now(),
        },
    )


@seller_required
def cancel_booking(request, booking_id):
    if request.method != 'POST':
        return redirect('bazaar:my_bookings')

    booking = get_object_or_404(BazaarBooking, pk=booking_id, seller=request.user)

    if booking.status == 'cancelled':
        messages.info(request, 'Booking already cancelled.')
        return redirect('bazaar:my_bookings')

    if booking.bazaar.start_datetime <= timezone.now():
        messages.error(request, 'You cannot cancel after the bazaar has started.')
        return redirect('bazaar:my_bookings')

    booking.status = 'cancelled'
    booking.save(update_fields=['status'])
    Notification.objects.create(
        recipient=booking.bazaar.organizer,
        sender=request.user,
        title='Bazaar Booking Cancelled',
        message=f'{request.user.username} cancelled booking for bazaar "{booking.bazaar.title}".',
        notification_type='bazaar_booking_cancelled',
        url=reverse('bazaar:organizer_bookings'),
    )
    messages.success(request, 'Booking cancelled.')
    return redirect('bazaar:my_bookings')


@bazar_organizer_required
def organizer_bookings(request):
    bookings = (
        BazaarBooking.objects.filter(bazaar__organizer=request.user)
        .select_related('bazaar', 'seller')
        .order_by('-created_at')
    )
    return render(request, 'bazaar/organizer_bookings.html', {'bookings': bookings})


@bazar_organizer_required
def update_booking_status(request, booking_id, status):
    if request.method != 'POST':
        return redirect('bazaar:organizer_bookings')

    if status not in {'approved', 'rejected'}:
        messages.error(request, 'Invalid status.')
        return redirect('bazaar:organizer_bookings')

    booking = get_object_or_404(
        BazaarBooking,
        pk=booking_id,
        bazaar__organizer=request.user,
    )

    if booking.status != 'pending':
        messages.info(request, 'Only pending bookings can be updated.')
        return redirect('bazaar:organizer_bookings')

    booking.status = status
    booking.save(update_fields=['status'])
    if status == 'approved':
        Notification.objects.create(
            recipient=booking.seller,
            sender=request.user,
            title='Bazaar Booking Approved',
            message=f'Your booking for bazaar "{booking.bazaar.title}" was approved.',
            notification_type='bazaar_booking_approved',
            url=reverse('bazaar:my_bookings'),
        )
    else:
        Notification.objects.create(
            recipient=booking.seller,
            sender=request.user,
            title='Bazaar Booking Rejected',
            message=f'Your booking for bazaar "{booking.bazaar.title}" was rejected.',
            notification_type='bazaar_booking_rejected',
            url=reverse('bazaar:my_bookings'),
        )

    if status == 'approved':
        messages.success(request, 'Booking approved')
    else:
        messages.success(request, 'Booking rejected')

    return redirect('bazaar:organizer_bookings')
