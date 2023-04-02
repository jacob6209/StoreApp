from itertools import product
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken,TokenError

from storeapp.models import Category, Product, Review, Cart, Cartitems, ProductImage,Profile
from django.contrib.auth import get_user_model
# from models import MyOrder,MyOrderItem
from rest_framework import serializers
User=get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "title", "slug"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image"]


class ProductSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()
    images = ProductImageSerializer(many=True, read_only=True)
    category=serializers.StringRelatedField()
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = Product
        fields = ["id", "name", "description","category", "inventory", "price", "images", "uploaded_images","user"]

    # serializer Relationships fields                =>   #9Y
    #     category=serializers.StringRelatedField()
    # code bellow show all CategorySerializer fields
    # category = CategorySerializer()

    def create(selfse, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        product = Product.objects.create(**validated_data)
        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)
        return product


class ReviewSerializer(serializers.ModelSerializer):
    # user=serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ["id", "date_created", "name", "description","user"]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)


class SempleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price"]


class CartItemSerializer(serializers.ModelSerializer):
    product = SempleProductSerializer(many=False)
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = Cartitems
        fields = ["id", "cart", "product", "quantity", "sub_total"]

    def get_sub_total(self, cartitems=Cartitems):
        return cartitems.quantity * cartitems.product.price


class UpdateCartItemSerializer(serializers.ModelSerializer):
    # id=serializers.IntegerField(write_only=True)
    class Meta:
        model=Cartitems
        fields=["quantity"]


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("there is no product associated with the given id")

        return value

    def save(self, **kwargs):
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]
        cart_id = self.context["cart_id"]
        try:
            cartitem = Cartitems.objects.get(product_id=product_id, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()
            self.instance = cartitem

        except:
            # self.instance = Cartitems.objects.create(product_id=product_id, cart_id=cart_id, quantity=quantity)
            self.instance = Cartitems.objects.create( cart_id=cart_id,**self.validated_data)
        return self.instance

    class Meta:
        model = Cartitems
        fields = ["id", "product_id", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(read_only=True, many=True)
    # serializerMethodField there are two-way to define using method_name and using get world prefix
    grand_total = serializers.SerializerMethodField(method_name="main_total")

    class Meta:
        model = Cart
        fields = ["id", "items", "grand_total"]

    def main_total(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=Profile
        fields=["user","full_name","address"]
        # fields='__all__'


# ------------------------------------------------------------
# serializers.py

class NewCartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    User = get_user_model()
    items = CartItemSerializer(read_only=True, many=True)
    # serializerMethodField there are two-way to define using method_name and using get world prefix
    grand_total = serializers.SerializerMethodField(method_name="main_total")

    class Meta:
        model = Cart
        fields = ["id","user","items", "grand_total"]

    def main_total(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total




# class LogoutSerializer(serializers.ModelSerializer):
#     refresh=serializers.CharField()
#
#     def validate(self,attrs):
#        self.token=attrs['refresh']
#        return attrs
#
#     def save(self, **kwargs):
#
#      try:
#         RefreshToken(self.token).blacklist()
#      except TokenError:
#           self.fail('bad token')





