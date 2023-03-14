from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register("products",views.ProductViewSet)
router.register("categories",views.CategoriViewSet)

# two whay to defin Router for ViewSets(ModelViewSets)
urlpatterns = router.urls
# secend whay
urlpatterns = [
    path("", include(router.urls))
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

