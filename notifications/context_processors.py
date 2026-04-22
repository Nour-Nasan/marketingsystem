from .models import Notification
from django.db.models import Q
from chat.models import Conversation


def notifications_unread_count(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
        unread_chat_count = (
            Conversation.objects.filter(
                Q(buyer=request.user) | Q(seller=request.user),
                messages__is_read=False
            )
            .exclude(messages__sender=request.user)
            .distinct()
            .count()
        )
    else:
        unread_count = 0
        unread_chat_count = 0

    return {
        'notifications_unread_count': unread_count,
        'unread_chat_count': unread_chat_count,
    }
