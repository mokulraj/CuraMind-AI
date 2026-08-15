from .models import Notification


def notification_context(request):

    if not request.user.is_authenticated:

        return {
            "unread_notification_count": 0,
        }


    unread_count = (
        Notification.objects
        .filter(
            user=request.user,
            read_at__isnull=True,
)
        .count()
    )


    return {
        "unread_notification_count": unread_count,
    }