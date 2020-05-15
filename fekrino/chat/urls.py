from django.urls import path

from chat.views.apiViews import ChatListView, GetChatMessagesView

app_name = 'chat'

urlpatterns = [
    path('list/', ChatListView.as_view()),
    path('messages/period/', GetChatMessagesView.as_view()),
]