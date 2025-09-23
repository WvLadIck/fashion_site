from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_item, name="add_item"),
    path("items/", views.items_list, name="items_list"),
    path("api/items/", views.items_json, name="items_json"),
]
