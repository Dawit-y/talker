import json
from channels.generic.websocket import AsyncWebsocketConsumer
from core.models import Profile
from .models import Message
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender_id = self.scope['user'].id
        self.recipient_id = self.scope['url_route']['kwargs']['recipient_id']
        self.chat_room = self.get_chat_group_name(self.sender_id, self.recipient_id)

        self.chat_group_name = f'chat_{self.chat_room}'

        # Join chat room group
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        
    # Join user's own group
        await self.channel_layer.group_add(
            self.get_channel_name(),
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave chat room group
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = self.scope['user'].id

        # Save the message to the database
        await self.save_message(sender_id, self.recipient_id, message)

        # Send the message to the chat room group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'sender_id': sender_id,
                'message': message
            }
        )
         # Send the message to the recipient's own group
        await self.channel_layer.group_send(
            f"user_{self.recipient_id}",
            {
                'type': 'chat_message',
                'sender_id': sender_id,
                'message': message
            }
        )

    async def chat_message(self, event):
        sender_id = event['sender_id']
        message = event['message']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'sender_id': sender_id,
            'message': message
        }))

    @staticmethod
    def get_chat_group_name(sender_id, recipient_id):
        return f'chat_{sender_id}_{recipient_id}'
    
    def get_channel_name(self):
        return f"user_{self.scope['user'].id}"

    @database_sync_to_async
    def save_message(self, sender_id, recipient_id, message):
        sender = Profile.objects.get(id=sender_id)
        recipient = Profile.objects.get(id=recipient_id)

        message_obj = Message(sender=sender, recipient=recipient, content=message)
        message_obj.save()
