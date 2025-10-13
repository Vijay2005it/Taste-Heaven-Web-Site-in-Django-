from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    USER_TYPE_CHOICE = (
        ('user', 'User'),
        ('admin', 'Admin')
    )

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICE, default='user')

    def __str__(self):
        return self.username


class FoodItem(models.Model):
    CATEGORY_CHOICE = (
        ('veg', 'Vegetarian'),
        ('non-veg', 'Non-Vegetarian'),
        ('drinks', 'Drinks'),
        ('dessert', 'Dessert')
    )
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='food_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    @property
    def total_price(self):
        return self.quantity * self.item.price

    def __str__(self):
        return f"{self.user.username} - {self.item.name} x {self.quantity}"



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.caption} (Gallery Image {self.id})"


class GalleryOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gallery_item = models.ForeignKey('Gallery', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_at = models.DateTimeField(auto_now_add=True)
    
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    @property
    def total_price(self):
        return self.quantity * self.gallery_item.price

    def __str__(self):
        return f"{self.user.username} - {self.gallery_item.caption} x {self.quantity}"




class Payments(models.Model):
    PAY_METHOD_CHOICES = [
        ('credit', 'Credit Card'),
        ('debit', 'Debit Card'),
        ('upi', 'UPI')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField()
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=50, choices=PAY_METHOD_CHOICES)
    bank_on_card = models.CharField(max_length=50, blank=True, null=True)
    card_number = models.CharField(max_length=50, blank=True, null=True)
    expiration_date = models.CharField(max_length=50, blank=True, null=True)
    cvv = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.first_name} {self.last_name} - {self.created_at.strftime('%Y-%m-%d')}"
    
class FeedBack(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    message = models.TextField()
    rating = models.IntegerField(choices=[(1, '⭐'), (2, '⭐⭐'), (3, '⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (5, '⭐⭐⭐⭐⭐')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Feedback From  {self.user.username} on {self.rating}⭐"