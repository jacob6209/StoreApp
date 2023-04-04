from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from api.cart import Cart

class CartToOrderView(APIView):
    authentication_classes = JWTAuthentication,
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart(request)
        if request.auth is None:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        if len(cart) == 0:
            return Response({"Error": "No Cart Items Found."}, status=status.HTTP_404_NOT_FOUND)

            # Check if required fields are not empty
        required_fields = ['first_name', 'last_name', 'phone_number', 'address']
        for field in required_fields:
            if not request.data.get(field):
                return Response({f"error: {field} is required."}, status=status.HTTP_400_BAD_REQUEST)

        # first_name = request.data.get('first_name')
        # last_name = request.data.get('last_name')
        #
        # if not first_name:
        #     return Response({"Error": "First name is required."}, status=status.HTTP_400_BAD_REQUEST)
        #
        # if not last_name:
        #     return Response({"Error": "Last name is required."}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user,
                                     firs_name=request.data.get('first_name'),
                                     last_name=request.data.get('last_name'),
                                     phone_number=request.data.get('phone_number'),
                                     address=request.data.get('address'),
                                     orders_notes=request.data.get('orders_notes'))

        for item in cart:
            product = item['product_obj']
            OrderItem.objects.create(order=order,
                                     product=product,
                                     quantity=item['quantity'],
                                     price=product.price)

        cart.clear()

        # ---------------  Save Some User info ------------
        request.user.first_name=order.firs_name
        request.user.last_name = order.last_name
        request.user.save()

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
