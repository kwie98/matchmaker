from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("items/", views.items, name="items"),
    path("item/<int:item_id>/", views.item, name="items"),
]
