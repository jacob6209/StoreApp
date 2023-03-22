from urllib import response

from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localdate
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

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

class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):

    http_method_names = ["post","delete","get","patch"]

    # queryset =Cartitems.objects.all()
    def get_queryset(self):
        return Cartitems.objects.filter(cart_id=self.kwargs['cart_pk'])

    def get_serializer_class(self):
        if self.request.method=="POST":
            return AddCartItemSerializer
        elif self.request.method=="PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id":self.kwargs["cart_pk"]}

    # serializer_class =CartItemSerializer

class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class= ProfileSerializer

#
# class LogoutAPIView(generics.GenericAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response({'LogOut':"Success"},status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response({'LogOut':"failed"},status=status.HTTP_400_BAD_REQUEST)

    # from djoser.views import TokenDestroyView
    # from djoser import utils
    #
    # class UserLogoutView(TokenDestroyView):
    #
    #     def post(self, request):
    #         return Response(status=status.HTTP_204_NO_CONTENT)


    # serializer_class = LogoutSerializer
    # permission_classes = permissions.IsAuthenticated,
    #
    # def post(self,request):
    #     serializer=self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

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

