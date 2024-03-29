from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from match.views.matchViews import LikeUserView, DislikeUserView, SuperLikeUserView

urlpatterns = {
    url(r'^like/$', LikeUserView.as_view(), name="like-user"),
    url(r'^superlike/$', SuperLikeUserView.as_view(), name="superlike-user"),
    url(r'^dislike/$', DislikeUserView.as_view(), name="dislike-user"),
}
urlpatterns = format_suffix_patterns(urlpatterns)