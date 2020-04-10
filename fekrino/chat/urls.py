from django.urls import path

from chat.views.apiViews import ChatListView, ChatCreateView, ChatDetailView, ChatUpdateView, ChatDeleteView

app_name = 'chat'

urlpatterns = [
    path('', ChatListView.as_view()),
    path('create/', ChatCreateView.as_view()),
    path('<pk>', ChatDetailView.as_view()),
    path('<pk>/update/', ChatUpdateView.as_view()),
    path('<pk>/delete/', ChatDeleteView.as_view())
]