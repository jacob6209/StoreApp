from urllib import response

from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localdate
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from config import settings
from .serializers import ProductSerializer, CategorySerializer,ReviewSerializer,CartSerializer,\
    CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer,ProfileSerializer
from storeapp.models import Category, Product,Review,Cart,Cartitems,Profile
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from api import serializers
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework import permissions
from config.permission import ProductViewSetPermission,ReviewViewSetPermission

# Create your views here.
# # === >  class based on ViewSet or  ModelViewSet  < =====

class ProductViewSet(ModelViewSet):
    permission_classes = [ProductViewSetPermission,]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=ProductFilter
    search_fields=['name','description']
    ordering_fields=['price']
    pagination_class = PageNumberPagination
    # filterset_fields=["category_id","price"]

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            return Response({"Message": "Failed"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"Message":"Success"},status=status.HTTP_204_NO_CONTENT)


class CategoriViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class= CategorySerializer


class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all()
    permission_classes = [ReviewViewSetPermission,]
    serializer_class = ReviewSerializer

    def get_queryset(self):
      return Review.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id":self.kwargs["product_pk"]}

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            return Response({"Message": "Failed"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"Message":"Success"},status=status.HTTP_204_NO_CONTENT)

# class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#
# class CartItemViewSet(ModelViewSet):
#
#     http_method_names = ["post","delete","get","patch"]
#
#     # queryset =Cartitems.objects.all()
#     def get_queryset(self):
#         return Cartitems.objects.filter(cart_id=self.kwargs['cart_pk'])
#
#     def get_serializer_class(self):
#         if self.request.method=="POST":
#             return AddCartItemSerializer
#         elif self.request.method=="PATCH":
#             return UpdateCartItemSerializer
#         return CartItemSerializer
#
#     def get_serializer_context(self):
#         return {"cart_id":self.kwargs["cart_pk"]}
#
#     # serializer_class =CartItemSerializer

class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class= ProfileSerializer
#     -----------------------------------------------------New Cart Using Session Method---------------------------
from rest_framework.decorators import api_view
from rest_framework.response import Response
from storeapp.models import Product
from .cart import Cart

@api_view(['POST'])
def add_to_cart(request):
    """
    Add a product to the cart
    """
    product_id = request.POST.get('product_id')
    quantity = request.data.get('quantity', 1)
    replace_current_quantity=request.data.get('replace_current_quantity',False)

    if not product_id:
        return Response({'error': 'Product ID is required'}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

    cart = Cart(request)
    cart.add(product, quantity=quantity,replace_current_quantity=replace_current_quantity)

    return Response({'message': 'Product added to cart'}, status=200)

@api_view(['POST'])
def remove_from_cart(request):
    """
    Remove a product from the cart
    """
    product_id = request.data.get('product_id')

    if not product_id:
        return Response({'error': 'Product ID is required'}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

    cart = Cart(request)
    cart.remove(product)

    return Response({'message': 'Product removed from cart'}, status=200)

@api_view(['POST'])
def clear_cart(request):
    """
    Remove all products from the cart
    """
    cart = Cart(request)
    cart.clear()

    return Response({'message': 'Cart cleared'}, status=200)

@api_view(['GET'])
def view_cart(request):
    """
    View the contents of the cart
    """
    cart = Cart(request)

    cart_items = []
    for item in cart:
        cart_items.append({
            'product_id': item['product_obj'].id,
            'product_name': item['product_obj'].name,
            'quantity': item['quantity'],
            'price': item['product_obj'].price,
            'sub_total': item['total_price']
        })

    return Response({'cart': cart_items, 'grand_total': cart.get_total_price(), 'Cart_len': len(cart)}, status=200)




