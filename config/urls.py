from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView # for swagger ui
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView # account login, register
from accounts.views import SuperUserTokenObtainPairView
from accounts.serializers import TenantEmailTokenObtainPairSerializer
from accounts import views as accounts_views
from companys import views as company_views
from customers import views as customer_views
from managers import views as manager_views
from technicians import views as technician_views
from hr import views as hr_views
from assets import views as assets_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/admin/login/', SuperUserTokenObtainPairView.as_view(), name='superuser_login'),

    path('api/<slug:company_slug>/login', TokenObtainPairView.as_view(serializer_class=TenantEmailTokenObtainPairSerializer), name='token_obtain_pair'),
    path('api/<slug:company_slug>/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),


    # Customer Registration and Profile
    path('api/<slug:company_slug>/customer/register', accounts_views.register, name='register'),
    path('api/<slug:company_slug>/customer/profile', customer_views.register, name='customer_profile'),

    path('api/<slug:company_slug>/me', accounts_views.me, name='me'),

    # Purifiers
    path('api/<slug:company_slug>/purifiers/', assets_views.purifier_list, name='purifier_list'),
    path('api/<slug:company_slug>/purifiers/create/', assets_views.purifier_create, name='purifier_create'),
    path('api/<slug:company_slug>/purifiers/<uuid:pk>/', assets_views.purifier_detail, name='purifier_detail'),
    path('api/<slug:company_slug>/my-purifier/', assets_views.my_purifier, name='my_purifier_details'),

    # SuperUserOnly : Company Creation
    path('api/secret/create-company', company_views.createCompany),

    # Owner Onboarding
    path('api/<slug:company_slug>/owner-onboarding', company_views.edit_owner_profile, name='owner_onboarding'),


    # Manager Onboarding
    path('api/<slug:company_slug>/managers/send-invite/', company_views.send_manager_invite, name='send_manager_invite'),
    path('api/managers/verify-invite/', manager_views.verify_invite_link, name='verify_manager_invite'),
    path('api/<slug:company_slug>/managers/accept-manager-invite/', manager_views.accept_manager_invite, name='accept_manager_invite'),
    path('api/<slug:company_slug>/managers/manager-onboarding/', manager_views.manager_onboarding, name='update_manager_profile'),


    # HR Onboarding
    path('api/<slug:company_slug>/hr/create-hr', hr_views.create_hr, name="create-hr"),


    # Technician Creating / Onboarding
    path('api/<slug:company_slug>/technician/create-technician', technician_views.create_technician, name="create-technician"),


    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
