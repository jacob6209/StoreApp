from urllib import response
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from .serializers import ProductSerializer, CategorySerializer
from storeapp.models import Category, Product
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from api import serializers
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
# # === >  class based on ViewSet or  ModelViewSet  < =====

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoriViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class= CategorySerializer




# class ApiProducts(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
# class ApiProduct(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
# class ApiCategories(ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class= CategorySerializer
#
# class ApiCategory(RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

# # === >   Class BaseView  < =====

# class ApiProducts(APIView):
#     def get(self,request):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
#
#     def post(self,request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

# class ApiProduct(APIView):
#     def get(self,request,pk):
#         product = get_object_or_404(Product, id=pk)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#
#     def put(self,request,pk):
#         product = get_object_or_404(Product, id=pk)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, id=pk)
#         product.delete()
#         return Response({'status': 'Success'}, status=status.HTTP_204_NO_CONTENT)


# class ApiCategories(APIView):
#     def get(self, request):
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)
#
#     def post(self,request):
#         serializer=CategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# class ApiCategory(APIView):
#     def get(self,request,pk):
#         category = get_object_or_404(Category, category_id=pk)
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)
#
#     def put(self,request,pk):
#         category = get_object_or_404(Category, category_id=pk)
#         serializer=CategorySerializer(category, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self,request,pk):
#         product = get_object_or_404(Product, id=pk)
#         product.delete()
#         return Response({'status': 'Success'}, status=status.HTTP_204_NO_CONTENT)








# # === >   Fanction BaseView  < =====
# @api_view(['GET','POST'])
# def api_products(request):
#     if request.method == "GET":
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
#     if request.method == "POST":
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
# @api_view(['GET','PUT','DELETE'])
# def api_product(request, pk):
#     product = get_object_or_404(Product, id=pk)
#     if request.method == "GET":
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     if request.method == "PUT":
#         serializer = ProductSerializer(product,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     if request.method == "DELETE":
#         product.delete()
#         return Response({'status':'True'},status=status.HTTP_204_NO_CONTENT)



# @api_view()
# def api_categories(request):
#     categories = Category.objects.all()
#     serializer = CategorySerializer(categories, many=True)
#     return Response(serializer.data)


# @api_view()
# def api_category(request, pk):
#     category = get_object_or_404(Category, category_id=pk)
#     serializer = CategorySerializer(category)
#     return Response(serializer.data)

