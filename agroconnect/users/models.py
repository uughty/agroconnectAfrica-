from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email_verified = models.BooleanField(default=False)

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sold = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

class Payment(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=(('pending', 'Pending'), ('received', 'Received')))
    escrow = models.BooleanField(default=True)

class Delivery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer_location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=(('pending', 'Pending'), ('delivered', 'Delivered')))

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=255)
    rating = models.IntegerField()
    comment = models.TextField()
