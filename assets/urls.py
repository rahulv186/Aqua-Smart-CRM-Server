from django.urls import path
from . import views

urlpatterns = [
    path('<slug:company_slug>/purifiers/', views.purifier_list, name='purifier_list'),
    path('<slug:company_slug>/purifiers/create/', views.purifier_create, name='purifier_create'),
    path('<slug:company_slug>/purifiers/<uuid:pk>/', views.purifier_detail, name='purifier_detail'),
]
