from django.contrib import admin

# Register your models here.

from .models import CustomUser, Manufacturer, Part, ShoppingCart, CartItem, Order, Delivery

admin.site.register(CustomUser)
admin.site.register(Manufacturer)
admin.site.register(Part)
admin.site.register(ShoppingCart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Delivery)