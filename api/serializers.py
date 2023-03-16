from itertools import product
from rest_framework import serializers
from storeapp.models import Category, Product,Review,Cart,Cartitems,ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "title", "slug"]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True,read_only=True)
    uploaded_images=serializers.ListField(
        child=serializers.ImageField(max_length=1000000,allow_empty_file=False,use_url=False),
        write_only=True
    )
    class Meta:
        model = Product
        fields = ["id", "name", "description","inventory", "price", "images","uploaded_images"]

    # serializer Relationships fields                =>   #9Y
    #     category=serializers.StringRelatedField()
    # code bellow show all CategorySerializer fields
    # category = CategorySerializer()

    def create(selfse, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        product = Product.objects.create(**validated_data)
        for image in uploaded_images:
            newproduct_image = ProductImage.objects.create(product=product, image=image)

        return product

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=["id","date_created","name","description"]

    def create(self, validated_data):
        product_id=self.context["product_id"]
        return Review.objects.create(product_id=product_id,**validated_data)

class SempleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","name","price"]

class CartItemSerializer(serializers.ModelSerializer):
    product = SempleProductSerializer(many=False)
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = Cartitems
        fields = ["id", "cart", "product", "quantity", "sub_total"]

    def get_sub_total(self,cartitems=Cartitems):
        return cartitems.quantity * cartitems.product.price




class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(read_only=True,many=True)
    # serializerMethodField there are two-way to define using method_name and using get world prefix
    grand_total = serializers.SerializerMethodField(method_name="main_total")

    class Meta:
        model = Cart
        fields = ["id", "items","grand_total"]

    def main_total(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total
