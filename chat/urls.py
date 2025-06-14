from django.urls import path

from .views import ChatSessionView, DetailChatSessionView, ChatSessionMessagesView


urlpatterns = [
    path('sessions/', ChatSessionView.as_view(), name='chat_sessions'),
    path('sessions/<uuid:pk>/', DetailChatSessionView.as_view(), name='detail_chat_session'),
    path('sessions/<uuid:pk>/messages/', ChatSessionMessagesView.as_view(), name='messages'),
]
