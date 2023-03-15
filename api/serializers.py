from itertools import product
from rest_framework import serializers
from storeapp.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "title", "slug"]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "category", "slug","image","inventory", "price"]

    # serializer Relationships fields                =>   #9Y
    #     category=serializers.StringRelatedField()
    # code bellow show all CategorySerializer fields
    category=CategorySerializer()


