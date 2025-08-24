from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # enforce unique email
    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"  # login with email instead of username
    REQUIRED_FIELDS = ["username"]  # username still required when creating superuser

    def __str__(self):
        return self.email


class Product(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sold = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Payment(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=50,
        choices=(('pending', 'Pending'), ('received', 'Received'))
    )
    escrow = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.seller} - {self.amount}"


class Delivery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer_location = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=(('pending', 'Pending'), ('delivered', 'Delivered'))
    )

    def __str__(self):
        return f"{self.product.name} - {self.status}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=255)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.buyer_name} - {self.rating}"
