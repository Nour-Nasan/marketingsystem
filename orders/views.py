from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from baskets.models import Basket
from notifications.models import Notification
from .forms import OrderOptionsForm
from users.decorators import buyer_required, seller_required
from .models import Order, OrderItem, OrderTracking


# ================== Tracking Flow ==================
TRACKING_FLOW = [
    'preparing',
    'prepared',
    'shipping',
    'delivered',
]


# ================== Seller Views ==================

@seller_required
def view_orders(request):
    seller = request.user

    orders = Order.objects.filter(
        items__product__shop__owner=seller,
        status__in=['pending', 'approved']
    ).distinct()

    return render(request, 'orders/view_orders.html', {
        'orders': orders
    })


@seller_required
def approve_order(request, order_id):
    seller = request.user
    order = get_object_or_404(
        Order.objects.filter(
            id=order_id,
            items__product__shop__owner=seller
        ).distinct()
    )

    if request.method == 'POST':
        if order.status == 'approved':
            return redirect('orders:order_details', order_id=order.id)

        order.approve()

        OrderTracking.objects.create(
            order=order,
            status='preparing'
        )
        Notification.objects.create(
            recipient=order.buyer,
            sender=request.user,
            title='Order Approved',
            message=f'Your order #{order.id} has been approved.',
            notification_type='order_approved',
            url=reverse('orders:my_orders'),
        )
        Notification.objects.create(
            recipient=order.buyer,
            sender=request.user,
            title='Order Status Updated',
            message=f'Order #{order.id} status updated to preparing.',
            notification_type='order_status_updated',
            url=reverse('orders:my_orders'),
        )

        return redirect('orders:order_details', order_id=order.id)

    return render(request, 'orders/approve_order.html', {'order': order})



@seller_required
def update_order_tracking(request, order_id):

    order = get_object_or_404(
        Order.objects.filter(
            id=order_id,
            items__product__shop__owner=request.user,
            status='approved'
        ).distinct()
    )

    last_tracking = order.tracking_steps.order_by('-updated_at').first()

    if last_tracking:
        current_index = TRACKING_FLOW.index(last_tracking.status)
    else:
        current_index = -1 

    if current_index + 1 >= len(TRACKING_FLOW):
        return redirect('orders:order_details', order_id=order.id)

    next_status = TRACKING_FLOW[current_index + 1]

    if request.method == 'POST':
        latest_tracking = order.tracking_steps.order_by('-updated_at').first()
        if latest_tracking and latest_tracking.status == next_status:
            return redirect('orders:order_details', order_id=order.id)

        OrderTracking.objects.create(
            order=order,
            status=next_status
        )
        Notification.objects.create(
            recipient=order.buyer,
            sender=request.user,
            title='Order Status Updated',
            message=f'Order #{order.id} status updated to {next_status}.',
            notification_type='order_status_updated',
            url=reverse('orders:my_orders'),
        )

        if next_status == 'delivered':
            order.status = 'delivered'
            order.save()

        return redirect('orders:order_details', order_id=order.id)

    return render(request, 'orders/update_order_tracking.html', {
        'order': order,
        'current_status': last_tracking.get_status_display() if last_tracking else 'Not started',
        'next_status': dict(OrderTracking.TRACKING_STATUS_CHOICES)[next_status]
    })


@seller_required
def reject_order(request, order_id):
    seller = request.user
    order = get_object_or_404(
        Order.objects.filter(
            id=order_id,
            items__product__shop__owner=seller
        ).distinct()
    )

    if request.method == 'POST':
        if order.status == 'rejected':
            return redirect('orders:view_orders')

        order.reject()
        Notification.objects.create(
            recipient=order.buyer,
            sender=request.user,
            title='Order Rejected',
            message=f'Your order #{order.id} has been rejected.',
            notification_type='order_rejected',
            url=reverse('orders:my_orders'),
        )
        return redirect('orders:view_orders')

    return render(request, 'orders/reject_order.html', {'order': order})


@seller_required
def order_details(request, order_id):
    order = get_object_or_404(
        Order.objects.filter(
            id=order_id,
            items__product__shop__owner=request.user
        ).distinct()
    )

    return render(request, 'orders/order_details.html', {'order': order})


# ================== Buyer Views ==================

@buyer_required
def create_order(request):
    basket = get_object_or_404(Basket, user=request.user)

    if not basket.items.exists():
        return redirect('baskets:view_basket')

    if request.method == 'POST':
        form = OrderOptionsForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                buyer=request.user,
                basket=basket,
                contact_method=form.cleaned_data['contact_method'],
                delivery_method=form.cleaned_data['delivery_method'],
                status='pending'
            )

            for item in basket.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )

            basket.items.all().delete()
            return redirect('orders:my_orders')
    else:
        form = OrderOptionsForm()

    return render(request, 'orders/confirm_order.html', {
        'form': form,
        'basket': basket
    })


@buyer_required
def my_orders(request):
    orders = Order.objects.filter(
        buyer=request.user
    ).order_by('-created_at')

    return render(request, 'orders/my_orders.html', {'orders': orders})

@buyer_required
def order_tracking(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        buyer=request.user,
        status='approved'
    )

    tracking_steps = order.tracking_steps.order_by('updated_at')

    return render(request, 'orders/order_tracking.html', {
        'order': order,
        'tracking_steps': tracking_steps
    })
