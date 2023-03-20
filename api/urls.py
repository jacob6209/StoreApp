from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


router=routers.DefaultRouter()
router.register("products",views.ProductViewSet)
router.register("categories",views.CategoriViewSet)
router.register("carts",views.CartViewSet)
router.register("userprofile",views.ProfileViewSet)

product_router=routers.NestedDefaultRouter(router,"products",lookup="product")
product_router.register("reviews",views.ReviewViewSet,basename="product-reviews")

cart_router=routers.NestedDefaultRouter(router,"carts",lookup="cart")
cart_router.register("items",views.CartItemViewSet,basename="cart-items")

# two-way to define Router for ViewSets(ModelViewSets)
# urlpatterns = router.urls
urlpatterns = [
    path("", include(router.urls)),
    path("",include(product_router.urls)),
    path("",include(cart_router.urls)),
    path("logout", views.LogoutAPIView.as_view(),name="logout")
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

