from django.urls import path
from . import views

urlpatterns = [
    path("items/", views.items_list, name="items_list"),

    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/clear/", views.cart_clear, name="cart_clear"),
    path("cart/add/<slug:slug>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<slug:slug>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/update/<int:item_id>/", views.update_cart, name="update_cart"),
    path("cart/delete/<slug:slug>/", views.delete_from_cart, name="delete_from_cart"),
    path("about/", views.about, name="about"),
    path("shop/checkout/", views.checkout, name="checkout"),
]
