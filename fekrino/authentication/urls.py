from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from authentication.views.PhoneActivationView import GetPhoneTokenView, VerifyPhoneTokenView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView)
urlpatterns = {
    url(r'^token/obtain/$', TokenObtainPairView.as_view(), name='get-jwt-token'),
    url(r'^token/refresh/$', TokenRefreshView.as_view(), name='refresh-jwt-token'),
    url(r'^token/verify/$', TokenVerifyView.as_view(), name='verify-jwt-token'),
    url(r'^otp/obtain/$', GetPhoneTokenView.as_view(), name='get-otp'),
    url(r'^otp/verify/$', VerifyPhoneTokenView.as_view(), name='verify-otp'),
}

urlpatterns = format_suffix_patterns(urlpatterns)