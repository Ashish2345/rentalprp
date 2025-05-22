from .models import Notification

def create_notification(user, title, message):
    """
    Creates and saves a new notification for a given user.

    Args:
        user (User): The user for whom the notification is created.
        title (str): The title of the notification.
        message (str): The message of the notification.

    Returns:
        Notification: The created notification instance.
    """
    notification = Notification(user=user, title=title, message=message)
    notification.save()
    return notification