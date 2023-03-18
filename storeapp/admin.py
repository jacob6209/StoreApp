from django.contrib import admin
from .models import *

# Register your models here.

# class ProductAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('name',)}
#
# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('title',)}
#

from storeapp.models import Cartitems

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)


class CartItemAdmin(admin.ModelAdmin):
    model = Cartitems
    list_display = ["product", "quantity", "get_cart_id"]

    def get_cart_id(self, obj):
        return obj.cart.id

    get_cart_id.short_description = 'Cart Id'
    get_cart_id.admin_order_field = 'cart__id'


admin.site.register(Cartitems, CartItemAdmin)
