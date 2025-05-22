from .models import Notification

def notification_list(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by("-id")
        noti_count = notifications.filter(viewed=False).count
    else:
        notifications = []
        noti_count = 0

    return {'notifications': notifications or [], "notification_count": noti_count or 0}
