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
      
     path("cart/", views.cart_view, name="cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/clear/", views.clear_cart, name="clear_cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
     path("list/", views.product_list, name="product_list"),
]
