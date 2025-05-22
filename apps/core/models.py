from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notification(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="noti_user")
	title = models.CharField(max_length=100, null=True, blank=True)
	message = models.CharField(max_length=512)
	viewed = models.BooleanField(default=False)