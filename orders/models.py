from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from storeapp.models import Cart,Profile
User = get_user_model()

#      Second Scenario
# class Order2(models.Model):
#     cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
#     user_profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     phone_number = models.CharField(max_length=20)
#     address = models.CharField(max_length=250)
#     order_notes = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f"Order {self.id}"

      # One Scenario
class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,default="")
    user=models.ForeignKey(User,verbose_name=_("User"),on_delete=models.CASCADE)
    is_paid=models.BooleanField(_("is paid"),default=False)
    firs_name=models.CharField(verbose_name=_("first name"),max_length=100)
    last_name=models.CharField(_("last name"),max_length=100)
    phone_number= models.CharField(_("phone number"),max_length=15)
    address = models.CharField(_("address"),max_length=700)

    zarinpal_authority=models.CharField(max_length=255,blank=True)

    orders_notes=models.CharField(_("Order Note"),max_length=700,blank=True)
    datatime_create = models.DateTimeField(_("create date"),auto_now_add=True)
    datatime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order{self.id}'

    def get_total_price(self):
        # result=0
        # for item in self.items.all():
        #     result+=(item.price*item.quantity)
        # return result
        return sum(item.quantity*item.price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,verbose_name=_("order"), on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey('storeapp.Product',verbose_name=_("Product"), on_delete=models.CASCADE,related_name='order_items')
    quantity=models.PositiveIntegerField(_("quantity"),default=1)
    price=models.PositiveIntegerField(_("Price"),)

    def __str__(self):
        return f'OrderItem{self.id} : {self.product} * {self.quantity} (price:{self.price})'









