from django.contrib import admin

from .models import Order, Product, Customer, Cart, CartItem

# Register your models here.
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartItem)