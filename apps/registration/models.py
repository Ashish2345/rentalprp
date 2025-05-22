from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=255)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(User, null=True, related_name='customer', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
