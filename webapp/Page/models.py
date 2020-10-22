from django.db import models
from django.contrib.auth.models import User


class Custumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    sex_choice = (
        ('1', 'Nam'),
        ('2', 'Nữ'),
        ('3', 'Khác'),
    )
    type_choice = (
        ('AD', 'Admin'),
        ('MN', 'Manager'),
        ('US', 'User'),
    )
    type = models.CharField(max_length=10, choices=type_choice, default='US')
    name = models.TextField(max_length=100, default='')
    sex = models.CharField(max_length=10, choices=sex_choice, default='1')
    age = models.IntegerField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    address = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    img = models.FileField(upload_to='pro_image', null=True, blank=True)
    price = models.FloatField(default=0, null=True, blank=True)
    is_sale = models.BooleanField(default=False)
    price_sale = models.FloatField(default=0, null=True, blank=True)
    choice = models.BooleanField(default=False)
    TTs = models.TimeField(auto_now=True)
    TTe = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class Cart(models.Model):
    product = models.ForeignKey(Product, related_name='by_product', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='by_cart', null=True, blank=True)
    num = models.IntegerField(default=0, null=True, blank=True)
    sum_product = models.FloatField(default=0, null=True, blank=True)
    is_pay = models.BooleanField(default=False)
    TTs = models.DateTimeField(auto_now=True)
    TTes = models.DateTimeField(editable=False, null=True, blank=True)
    confirm = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    is_old = models.BooleanField(default=False)

    def __str__(self):
        return self.product.title


