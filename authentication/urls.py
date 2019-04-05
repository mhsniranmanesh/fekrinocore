from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token, ObtainJSONWebToken
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from authentication.views.PhoneActivationView import GetPhoneTokenView, VerifyPhoneTokenView

urlpatterns = {
    url(r'^token/obtain/$', obtain_jwt_token, name='get-jwt-token'),
    url(r'^token/refresh/$', refresh_jwt_token, name='refresh-jwt-token'),
    url(r'^token/verify/$', verify_jwt_token, name='verify-jwt-token'),
    url(r'^otp/obtain/$', GetPhoneTokenView.as_view(), name='get-otp'),
    url(r'^otp/verify/$', VerifyPhoneTokenView.as_view(), name='verify-otp'),
    # url(r'^otp/verify/$', GetPhoneTokenView, name='verify-jwt-token'),
}

urlpatterns = format_suffix_patterns(urlpatterns)