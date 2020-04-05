from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from fekrino.authentication.views.PhoneActivationView import GetPhoneTokenView, VerifyPhoneTokenView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = {
    url(r'^token/obtain/$', TokenObtainPairView, name='get-jwt-token'),
    url(r'^token/refresh/$', TokenRefreshView, name='refresh-jwt-token'),
    url(r'^otp/obtain/$', GetPhoneTokenView.as_view(), name='get-otp'),
    url(r'^otp/verify/$', VerifyPhoneTokenView.as_view(), name='verify-otp'),
}

urlpatterns = format_suffix_patterns(urlpatterns)