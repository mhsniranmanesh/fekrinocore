from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from profiles.views.profilePictureViews import ProfilePictureView, SetProfilePicturePriorityView
from profiles.views.userViews import UserUpdateInfosView, UserUpdateLocationView, UserGetInitialInfosView

urlpatterns = {
    url(r'^initial/$', UserGetInitialInfosView.as_view(), name="user-initial"),
    url(r'^location/update/$', UserUpdateLocationView.as_view(), name="update-location"),
    url(r'^infos/update/$', UserUpdateInfosView.as_view(), name="update-profile-infos"),
    url(r'^picture/$', ProfilePictureView.as_view(), name="set-profile-picture"),
    url(r'^picture/set-priority/$', SetProfilePicturePriorityView.as_view(), name="set-profile-picture-priority"),
}
urlpatterns = format_suffix_patterns(urlpatterns)