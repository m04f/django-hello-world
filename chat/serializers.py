from rest_framework import serializers

from .models import Message, ChatSession

class MessageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=1000)
    role = serializers.ChoiceField(choices=Message.ROLE_CHOICES)

    class Meta:
        model = Message
        fields = ['content', 'role', 'timestamp']

class ChatSessionSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(
        view_name='detail_chat_session',
    )
    class Meta:
        model = ChatSession
        fields = ['uuid', 'title', 'created_at', 'details']

class DetailChatSessionSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True, source='message_set')

    class Meta:
        model = ChatSession
        fields = ['uuid', 'title', 'created_at', 'messages']
