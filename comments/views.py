from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from orders.models import OrderItem
from products.models import Product
from notifications.models import Notification
from .models import Comment
from .forms import CommentForm
from orders.models import OrderTracking


def buyer_can_comment(user, product):
    if not user.is_authenticated:
        return False

    if getattr(user, 'role', None) != 'buyer':
        return False
    
    return OrderItem.objects.filter(
    order__buyer=user,
    product=product,
    order__tracking_steps__status='delivered'
).exists()


def seller_owns_product(user, product):
    return (
        user.is_authenticated
        and getattr(user, 'role', None) == 'seller'
        and hasattr(user, 'shop')
        and product.shop.owner_id == user.id
    )



@login_required
def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not buyer_can_comment(request.user, product):
        messages.error(
            request,
            "You can only review this product after the order is delivered."
        )
        return redirect('products:product_detail', product_id=product.id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.parent = None  
            comment.save()

            seller_user = product.shop.owner
            if seller_user != request.user:
                Notification.objects.create(
                    recipient=seller_user,
                    sender=request.user,
                    title='New Product Comment',
                    message=f'You have a new comment on your product "{product.productName}".',
                    notification_type='new_product_comment',
                    url=reverse('products:product_detail', args=[product.id]),
                )
            return redirect('products:product_detail', product_id=product.id)
    else:
        form = CommentForm()

    return render(request, 'comments/add_comment.html', {
        'form': form,
        'product': product
    })



@login_required
def add_reply(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    product = parent_comment.product

    allowed = (
        seller_owns_product(request.user, product)
        or buyer_can_comment(request.user, product)
    )

    if not allowed:
        messages.error(request, "You are not allowed to reply here.")
        return redirect('products:product_detail', product_id=product.id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.product = product
            reply.parent = parent_comment
            reply.save()

            seller_user = product.shop.owner
            if seller_user != request.user:
                Notification.objects.create(
                    recipient=seller_user,
                    sender=request.user,
                    title='New Reply on Product Comment',
                    message=f'You have a new reply on comments for your product "{product.productName}".',
                    notification_type='product_comment_reply',
                    url=reverse('products:product_detail', args=[product.id]),
                )

            if (
                parent_comment.user != request.user
                and getattr(parent_comment.user, 'role', None) == 'buyer'
            ):
                Notification.objects.create(
                    recipient=parent_comment.user,
                    sender=request.user,
                    title='Reply to Your Comment',
                    message=f'Someone replied to your comment on "{product.productName}".',
                    notification_type='reply_to_comment',
                    url=reverse('products:product_detail', args=[product.id]),
                )

    return redirect('products:product_detail', product_id=product.id)
