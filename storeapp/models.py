from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import User
User = get_user_model()


# from  django.conf import settings
# from UserProfile.models import Customer

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=200)
    category_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    slug = models.SlugField(default=None)
    featured_product = models.OneToOneField('Product', on_delete=models.CASCADE, blank=True, null=True,
                                            related_name='featured_product')
    icon = models.CharField(max_length=100, default=None, blank=True, null=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review')

    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="reviews")
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default="description")
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class Product(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='product')

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    discount = models.BooleanField(default=False)
    image = models.ImageField(upload_to='img', blank=True, null=True, default='')
    price = models.FloatField(default=100.00)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    slug = models.SlugField(default=None,blank=True,null=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    inventory = models.IntegerField(default=5)
    top_deal = models.BooleanField(default=False)
    flash_sales = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Cartitems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True,related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='cartitems')
    quantity = models.PositiveIntegerField(default=0)


class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")
    image=models.ImageField(upload_to='img',default="",null=True,blank="")


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True,default="")
    full_name=models.CharField(max_length=30)
    address=models.TextField()

    # def __str__(self):
    #     return str(self.user)

# class TestOrder(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    # is_paid=models.BooleanField(_("is paid"),default=False)
    # firs_name=models.CharField(verbose_name=_("first name"),max_length=100)
    # last_name=models.CharField(_("last name"),max_length=100)
    # phone_number= models.CharField(_("phone number"),max_length=15)
    # address = models.CharField(_("address"),max_length=700,default="")
    # zarinpal_authority=models.CharField(max_length=255,blank=True)
    # orders_notes=models.CharField(_("Order Note"),max_length=700,blank=True)
    # datatime_create = models.DateTimeField(_("create date"),auto_now_add=True)
    # datatime_modified = models.DateTimeField(auto_now=True)
    #
    # def __str__(self):
    #     return f'Order{self.id}'
    #
    # def get_total_price(self):
    #     # result=0
    #     # for item in self.items.all():
    #     #     result+=(item.price*item.quantity)
    #     # return result
    #     return sum(item.quantity*item.price for item in self.items.all())

# class TestOrderItem(models.Model):
#     order = models.ForeignKey(TestOrder,verbose_name=_("order"), on_delete=models.CASCADE)
#     product=models.ForeignKey(Product,verbose_name=_("Product"), on_delete=models.CASCADE)



# class SavedItem(models.Model):
#     owner = models.ForeignKey(Customer, on_delete=models.CASCADE, null = True, blank=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
#     added = models.IntegerField(default=0)


#     def __str__(self):
#         return str(self.id)

