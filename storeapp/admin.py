from django.contrib import admin
from .models import *
# Register your models here.

# class ProductAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('name',)}
#
# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('title',)}
#
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Cartitems)



