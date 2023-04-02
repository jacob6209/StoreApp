import requests
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .models import Order,OrderItem
from .serializers import OrderSerializer,OrderItemSerializer
from storeapp.models import Cartitems,Cart
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication

      # One Scenario

class CartToOrderView(APIView):
    def post(self, request, cart_id):
        # Get the current user's cart based on cart id
        cart = get_object_or_404(Cart, pk=cart_id)

        # Verify that the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the cart items
        cart_items = cart.items.all()

        # Verify that at least one cart item exists
        if not cart_items.exists():
            return Response({"error": "No cart items found for specified cart ID."}, status=status.HTTP_404_NOT_FOUND)

        # Create a new order based on the cart's contents
        order = Order.objects.create(cart=cart,
                                     user=request.user,
                                     firs_name=request.data.get('firs_name'),
                                     last_name=request.data.get('last_name'),
                                     phone_number=request.data.get('phone_number'),
                                     address=request.data.get('address'),
                                     orders_notes=request.data.get('orders_notes'))

        # Create an order item for each cart item
        for item in cart_items:
            OrderItem.objects.create(order=order,
                                     product=item.product,
                                     quantity=item.quantity,
                                     price=item.product.price)

        # # Clear the cart
        # cart.items.all().delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

  # Secend Scenario
# class CartToOrderView(APIView):
#     authentication_classes = (TokenAuthentication,)
#
#     def post(self, request, cart_id):
#         user = request.user  # get the authenticated user
#         cart = Cart.objects.get(id=cart_id)
#
#         # create the order
#         order = Order2.objects.create(
#             user=user,
#             cart=cart,
#             first_name=request.data.get('first_name'),
#             last_name=request.data.get('last_name'),
#             phone_number=request.data.get('phone_number'),
#             address=request.data.get('address'),
#             order_notes=request.data.get('order_notes')
#         )
#
#         # clear the cart
#         # cart.items.all().delete()
#
#         serializer = OrderSerializer(order)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)




class OrderCreateView(APIView):
    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response({'order_number': order.order_number}, status=201)
        return Response(serializer.errors, status=400)


                # ===== >  when we want use defult form (django form) we use bellow commend <=======
    # return render(request,'orders/order_create.html',context={
    #     'form':OrderForm(),
    # })
