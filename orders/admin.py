from django.contrib import admin
from .models import Order,OrderItem
from jalali_date.admin import ModelAdminJalaliMixin

# class CommentsInLine(admin.TabularInline):




class OrderItemInLine(admin.StackedInline):
   model = OrderItem
   fields = ['order','product','quantity','price',]
   extra = 1


@admin.register(Order)
class OrderAdmin(ModelAdminJalaliMixin,admin.ModelAdmin):
   list_display = ['user','datatime_create','firs_name','last_name','is_paid']

   inlines = [
      OrderItemInLine,
   ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
   list_display = ['product','quantity','price','order',]


