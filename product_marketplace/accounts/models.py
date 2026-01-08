from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Business(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('EDITOR', 'Editor'),
        ('APPROVER', 'Approver'),
        ('VIEWER', 'Viewer'),
    ]

    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, null=True, blank=True
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username
