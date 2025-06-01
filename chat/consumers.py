from channels.generic.websocket import AsyncWebsocketConsumer

import json

from .models import Message, ChatSession
from .chatbot import ChatBot


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.bot = None
        self.messages = []
        self.uuid = None

    async def connect(self):
        self.uuid = self.scope['url_route']['kwargs']['session']
        await self.accept()

        # Check if there are existing messages in the database
        async for msg in Message.objects.filter(session_id=self.uuid):
            self.messages.append(msg)

        self.bot = ChatBot(self.uuid)

    async def disconnect(self, code):
        pass

    async def send_message(self, message: Message):
        await self.send(text_data=json.dumps({'message': message.content, 'role': message.role, 'timestamp': str(message.timestamp)}))

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            if text_data_json['message']:
                message = text_data_json['message']
                db_message = await Message.objects.acreate(session_id=self.uuid, role='user', content=message)
                self.messages.append(db_message)
                await self.send_message(db_message)

                # Call the chat model
                response = await self.bot.send_message(self.messages)
                await Message.objects.abulk_create(response)
                await self.send_message(response[-1])
