from django.contrib import admin

from .models import Cart, Product, Custumer

# Register your models here.
admin.site.register(Cart)
admin.site.register(Product)
admin.site.register(Custumer)
