from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ChatSession, Message
from .serializers import ChatSessionSerializer, DetailChatSessionSerializer, MessageSerializer
from .chatbot import ChatBot

class ChatSessionView(generics.ListAPIView, generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSessionSerializer

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user).all()

    def perform_create(self, serializer):
        session = serializer.save(user=self.request.user)


class DetailChatSessionView(generics.RetrieveAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DetailChatSessionSerializer

    def get_object(self):
        return get_object_or_404(ChatSession, pk=self.kwargs['pk'], user=self.request.user)


class ChatSessionMessagesView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(session=self.kwargs['pk'], session__user=self.request.user).all()

    def chatbot(self, pk):
        return ChatBot(pk)

    def post(self, request, pk, format=None):
        serializer = MessageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(session_id=pk)
        chatbot = self.chatbot(pk)
        messages = Message.objects.filter(session=self.kwargs['pk']).all()
        response = chatbot.send_message(list(messages))
        Message.objects.bulk_create(response)
        return Response(MessageSerializer(response[-1]).data, status=status.HTTP_201_CREATED)
