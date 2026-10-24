from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView # for swagger ui
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView # account login, register
from accounts.views import SuperUserTokenObtainPairView
from accounts.serializers import TenantEmailTokenObtainPairSerializer
from accounts import views as accounts_views
from companys import views as company_views
from managers import views as manager_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/admin/login/', SuperUserTokenObtainPairView.as_view(), name='superuser_login'),

    path('api/<slug:company_slug>/login', TokenObtainPairView.as_view(serializer_class=TenantEmailTokenObtainPairSerializer), name='token_obtain_pair'),
    path('api/<slug:company_slug>/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/<slug:company_slug>/register', accounts_views.register, name='register'),

    path('api/<slug:company_slug>/me', accounts_views.me, name='me'),

    # SuperUserOnly : Company Creation
    path('api/secret/create-company', company_views.createCompany),

    # Owner Onboarding
    path('api/<slug:company_slug>/owner-onboarding', company_views.edit_owner_profile, name='owner_onboarding'),


    # Manager Onboarding
    path('api/<slug:company_slug>/managers/send-invite/', company_views.send_manager_invite, name='send_manager_invite'),
    path('api/<slug:company_slug>/managers/verify-invite/', manager_views.verify_invite_link, name='verify_manager_invite'),
    path('api/<slug:company_slug>/managers/accept-manager-invite/', manager_views.accept_manager_invite, name='accept_manager_invite'),
    path('api/<slug:company_slug>/managers/manager_onboarding/', manager_views.manager_onboarding, name='update_manager_profile'),


    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
