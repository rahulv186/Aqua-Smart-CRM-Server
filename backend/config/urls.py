from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView # for swagger ui

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView # account login, register
from accounts.views import SuperUserTokenObtainPairView
from accounts import views as accounts_views
from companys import views as company_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/admin/login/', SuperUserTokenObtainPairView.as_view(), name='superuser_login'),

    path('api/<slug:company_slug>/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/<slug:company_slug>/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/<slug:company_slug>/register', accounts_views.register, name='register'),

    path('api/<slug:company_slug>/me', accounts_views.me, name='me'),
    path('api/secret/create-company', company_views.createCompany),



    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
