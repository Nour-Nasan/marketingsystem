from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from .models import Conversation, Message
from .forms import MessageForm
from shops.models import Shop
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def inbox(request):
    user = request.user
    is_buyer = user.role == 'buyer'
    is_seller = user.role == 'seller'

    conversations = Conversation.objects.filter(
        Q(buyer=user) | Q(seller=user)
    ).order_by('-last_updated')

    conversations_data = []
    for conv in conversations:
        unread_count = conv.messages.filter(
            is_read=False
        ).exclude(sender=user).count()

        conversations_data.append({
            'conversation': conv,
            'unread_count': unread_count
        })

    shops = None
    query = request.GET.get('q')

    if is_buyer:
        shops = Shop.objects.all()
        if query:
            shops = shops.filter(shopName__icontains=query)

    return render(request, 'chat/inbox.html', {
        'conversations_data': conversations_data,
        'shops': shops,
        'is_buyer': is_buyer,
        'is_seller': is_seller,
        'query': query,
    })


@login_required
def chat_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Security: Only participants can view
    if request.user != conversation.buyer and request.user != conversation.seller:
        return HttpResponseForbidden("You are not a participant in this conversation.")
    
    messages = conversation.messages.all()
    
    # Mark messages as read (incoming only)
    unread_messages = messages.filter(is_read=False).exclude(sender=request.user)
    unread_messages.update(is_read=True)
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()

            if request.user == conversation.seller:
                conversation.deleted_by_buyer = False
            elif request.user == conversation.buyer:
                conversation.deleted_by_seller = False

            conversation.save()

            return redirect('chat:chat_detail', conversation_id=conversation.id)
    else:
        form = MessageForm()
        
    return render(request, 'chat/chat_detail.html', {
        'conversation': conversation,
        'messages': messages,
        'form': form
    })

@login_required
def start_conversation(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    buyer = request.user
    seller = shop.owner

    if buyer == seller:
        return redirect('chat:inbox')

    conversation = Conversation.objects.filter(
        buyer=buyer,
        seller=seller,
        related_shop=shop
    ).first()

    if conversation:
        if conversation.deleted_by_buyer:
            conversation.deleted_by_buyer = False

            conversation.messages.all().delete()

            conversation.save()
    else:
        conversation = Conversation.objects.create(
            buyer=buyer,
            seller=seller,
            related_shop=shop
        )

    return redirect('chat:chat_detail', conversation_id=conversation.id)

@login_required
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    if request.user == conversation.buyer:
        conversation.deleted_by_buyer = True
    elif request.user == conversation.seller:
        conversation.deleted_by_seller = True
    else:
        return HttpResponseForbidden()

    conversation.save()
    return redirect('chat:inbox')

@login_required
def confirm_delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    # Security
    if request.user != conversation.buyer and request.user != conversation.seller:
        return HttpResponseForbidden()

    if request.method == 'POST':
        if request.user == conversation.buyer:
            conversation.deleted_by_buyer = True
        elif request.user == conversation.seller:
            conversation.deleted_by_seller = True

        conversation.save()
        return redirect('chat:inbox')

    return render(request, 'chat/confirm_delete_conversation.html', {
        'conversation': conversation
    })


@login_required
def buyer_shops(request):
    q = request.GET.get('q', '').strip()
    shops = Shop.objects.all()
    if q:
        shops = shops.filter(shopName__icontains=q)
    shops = shops.order_by('shopName')
    return render(request, 'chat/select_shop.html', {
        'shops': shops,
        'q': q
    })
