from django.db import models
from accounts.models import User, Business

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    business = models.ForeignKey(
        "accounts.Business",
        on_delete=models.CASCADE,
        related_name="products"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
