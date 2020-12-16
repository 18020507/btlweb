import uuid

from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # sex_choice = (
    #     ('Nam', 'Nam'),
    #     ('Nữ', 'Nữ'),
    #     ('Khác', 'Khác'),
    # )
    type_choice = (
        ('AD', 'Admin'),
        ('MN', 'Manager'),
        ('US', 'User'),
    )
    type = models.CharField(max_length=10, choices=type_choice, default='US')
    name = models.TextField(max_length=100, default='')
    # sex = models.CharField(max_length=10, choices=sex_choice, default='1')
    # age = models.IntegerField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    # address = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=3000, null=True, blank=True)
    img = models.FileField(upload_to='pro_image', null=True, blank=True)
    price = models.FloatField(default=0, null=True, blank=True)
    is_sale = models.BooleanField(default=False)
    price_sale = models.FloatField(default=0, null=True, blank=True)
    type = models.CharField(max_length=300, null=True, blank=True)
    size = models.CharField(max_length=10, null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)
    for_male = models.BooleanField(default=False)
    for_female = models.BooleanField(default=False)
    TTs = models.TimeField(auto_now=True)
    TTe = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class Cart(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.IntegerField(null=True, blank=True)
    CreateAt = models.DateTimeField(auto_now=True)
    is_new = models.BooleanField(default=True)
    is_pending = models.BooleanField(default=True)


class CartItem(models.Model):
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    id_cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    num = models.IntegerField(default=0, null=True, blank=True)
    sum_product = models.FloatField(default=0, null=True, blank=True)
    is_checked = models.BooleanField(default=False)


class Order(models.Model):
    id_cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status_choice = (
        ('pending', 'pending'),
        ('confirm', 'confirm'),
        ('paid', 'paid'),
        ('shipping', 'shipping'),
        ('completed', 'completed'),
    )
    status = models.CharField(max_length=10, choices=status_choice, null=True, blank=True)
    address = models.TextField(max_length=1000, null=True, blank=True)
