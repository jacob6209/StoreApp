
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(ModelViewSet):
    # permission_classes = [ReviewViewSetPermission,]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer




# from django.shortcuts import render,redirect
# from .forms import OrderForm
# from django.contrib.auth.decorators import login_required
# from cart.cart import Cart
# from .models import OrderItem
# from django.contrib import messages
# from django.utils.translation import gettext as _
#
# @login_required
# def order_create_view(request):
#     order_form=OrderForm()
#     cart=Cart(request)
#     if len(cart)==0:
#         messages.warning(request,_("You Can Not Proceed to Checkout Page Because Your Cart is Empty."))
#         return redirect("product_list")
#
#     if request.method=='POST':
#         order_form=OrderForm(request.POST,)
#         if order_form.is_valid():
#             order_obj=order_form.save(commit=False)
#             order_obj.user=request.user
#             order_obj.save()
#
#             for item in cart:
#                 product=item['product_obj']
#                 OrderItem.objects.create(
#                     order=order_obj,
#                     product=product,
#                     quantity=item['quantity'],
#                     price=product.price,
#                 )
#                 cart.clear()
#                 request.user.first_name=order_obj.firs_name
#                 request.user.last_name=order_obj.last_name
#                 request.user.save()
#
#                 request.session['order_id']=order_obj.id
#                 return redirect('payment:payment_process')
#
#     return render(request, 'orders/order_create.html',context={
#         'form':order_form,
#     })
#
#
#                 # ===== >  when we want use defult form (django form) we use bellow commend <=======
#     # return render(request,'orders/order_create.html',context={
#     #     'form':OrderForm(),
#     # })
