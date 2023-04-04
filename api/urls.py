from django.urls import path,include

import accounts.views
from . import views
from orders.views import OrderCreateView,CartToOrderView
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from django.urls import path, register_converter
from django.urls.converters import UUIDConverter
from .views import add_to_cart, remove_from_cart, clear_cart, view_cart

register_converter(UUIDConverter, 'UUID')

router=routers.DefaultRouter()
router.register("products",views.ProductViewSet)
router.register("categories",views.CategoriViewSet)
# router.register("carts",views.CartViewSet)

router.register("userprofile",views.ProfileViewSet)

# router.register("orders",OrderViewSet,basename="order")


product_router=routers.NestedDefaultRouter(router,"products",lookup="product")
product_router.register("reviews",views.ReviewViewSet,basename="product-reviews")

# cart_router=routers.NestedDefaultRouter(router,"carts",lookup="cart")
# cart_router.register("items",views.CartItemViewSet,basename="cart-items")

# child_order_router=routers.NestedDefaultRouter(router,"orders",lookup="cart")
# child_order_router.register("items",views.CartItemViewSet,basename="cart-items")


urlpatterns = [
    path("", include(router.urls)),
    path("",include(product_router.urls)),
    # path("",include(cart_router.urls)),

    # path("",include(child_order_router.urls)),
    # path('orders/<uuid:cart_id>/', OrderCreateView.as_view()),
    path('order/', CartToOrderView.as_view()),

    path('cart/add/', add_to_cart),
    path('cart/remove/', remove_from_cart),
    path('cart/clear/', clear_cart),
    path('cart/view/', view_cart),

]


# urlpatterns = [
#
#     path("products", views.ApiProducts.as_view()),
#     path("products/<str:pk>", views.ApiProduct.as_view()),
#     path("categories", views.ApiCategories.as_view()),
#     path("categories/<str:pk>", views.ApiCategory.as_view()),
# ]




#      ===== >  path for fanctionView  <=====
# urlpatterns = [
#     path("products", views.api_products),
#     path("products/<str:pk>", views.api_product),
#     path("categories", views.api_categories),
#     path("categories/<str:pk>", views.api_category),
# ]

