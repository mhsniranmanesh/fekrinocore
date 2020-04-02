from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from discover.views.findViews import FindNearView


urlpatterns = {
    url(r'^near/$', FindNearView.as_view(), name="find-near"),
}
urlpatterns = format_suffix_patterns(urlpatterns)