from .models import Notification


def notifications_unread_count(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
    else:
        unread_count = 0

    return {'notifications_unread_count': unread_count}
