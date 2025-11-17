"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from emailers.views import *
<<<<<<< HEAD
=======
from emailers.api_test import test_emailer_api, get_email_burst_stats
>>>>>>> b167811 (with working front and back)

urlpatterns = [
    # Default
    path('admin/', admin.site.urls),

    # Auth
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # EmailBurst
    path('api/email-burst/', EmailBurstListCreateAPIView.as_view()),
    path('api/email-burst/<int:pk>/', EmailBurstRetrieveUpdateDestroyAPIView.as_view()),
    path('api/email-burst/<int:pk>/send/', send_email_burst, name='send_email_burst'),
    path('api/email-burst/<int:pk>/schedule/', schedule_email_burst, name='schedule_email_burst'),
    path('api/email-burst/<int:pk>/stats/', get_email_burst_stats, name='get_email_burst_stats'),

    # Test endpoint
    path('api/test/emailer/', test_emailer_api, name='test_emailer_api'),

    # Members (Users)
    path('api/members/', MemberListCreateAPIView.as_view()),
    path('api/members/<int:pk>/', MemberRetrieveUpdateDestroyAPIView.as_view()),

    # Staff-specific endpoints
    path('api/staff/', StaffListAPIView.as_view(), name='staff-list'),
    path('api/staff/<int:pk>/', StaffRetrieveUpdateDestroyAPIView.as_view(), name='staff-detail'),

    # Non-staff (Members) endpoints
    path('api/non-staff/', NonStaffListAPIView.as_view(), name='non-staff-list'),
    path('api/non-staff/<int:pk>/', NonStaffRetrieveUpdateDestroyAPIView.as_view(), name='non-staff-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)