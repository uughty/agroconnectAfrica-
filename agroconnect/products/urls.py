from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    # Public
    path("", views.product_list, name="product_list"),
    path("<int:pk>/", views.product_detail, name="product_detail"),

    # Farmer
    path("mine/", views.my_products, name="my_products"),
    path("add/", views.add_product, name="add_product"),
    path("<int:pk>/edit/", views.edit_product, name="edit_product"),
    path("<int:pk>/delete/", views.delete_product, name="delete_product"),

    # Cart
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/clear/", views.clear_cart, name="clear_cart"),
    path("search/", views.product_search, name="product_search"),
]
