from django.urls import path
from . import views

urlpatterns = [
    path("", views.inventory_list_create, name="inventory-list-create"),
    path("<uuid:pk>/", views.inventory_detail, name="inventory-detail"),
]
