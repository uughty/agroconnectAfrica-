# agroconnect/products/models.py
from django.db import models
from django.conf import settings

class Category(models.TextChoices):
    LIVESTOCK = 'Livestock', 'Livestock'
    CROPS = 'Crops', 'Crops'
    FRUITS = 'Fruits', 'Fruits'
    VEGETABLES = 'Vegetables', 'Vegetables'
    GRAINS = 'Grains', 'Grains'
    OTHER = 'Other', 'Other'

class Product(models.Model):
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products"
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER
    )
    quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.category}"
        
