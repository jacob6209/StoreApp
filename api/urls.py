from django.urls import path
from . import views

urlpatterns = [

    path("products", views.ApiProducts.as_view()),
    path("products/<str:pk>", views.ApiProduct.as_view()),
    path("categories", views.ApiCategories.as_view()),
    path("categories/<str:pk>", views.ApiCategory.as_view()),
]




#      ===== >  path for fanctionView  <=====
# urlpatterns = [
#     path("products", views.api_products),
#     path("products/<str:pk>", views.api_product),
#     path("categories", views.api_categories),
#     path("categories/<str:pk>", views.api_category),
# ]

