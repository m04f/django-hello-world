from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import ChatSession
from .serializers import ChatSessionSerializer, DetailChatSessionSerializer

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
