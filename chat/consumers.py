import json
import time
import random
from channels.generic.websocket import WebsocketConsumer
from random import randint
from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asyncio import sleep
from asgiref.sync import async_to_sync

class chatConsumer(WebsocketConsumer):

    def connect(self):
       self.room_group_name = 'test'
       async_to_sync(self.channel_layer.group_add)(
           self.room_group_name,
           self.channel_name
       )
       self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]  
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type' : 'chat_message',
                'message' : message
            }
        )
    def chat_message(self,event):
        message = event['message']
        self.send(text_data=json.dumps({
            'type' : "chat",
            "message" : message
        }))

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

class DomainTwo:

    def do(self):
        value = random.randint(0,100)
        return json.dumps({'data': value})
class TwoConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        await self.accept()
        D = DomainTwo()
        for i in range(100):
            data = D.do()
            await self.send(data)
            await sleep(2)
class Domain:
    def do(self):
        word = randint(1,100)
        return json.dumps({"message": word})

class OneConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        D = Domain()
        for i in range(100):
            data = D.do()
            self.send(data)
            time.sleep(2)

# class ChatConsumer(AsyncConsumer):
#     async def websocket_connect(self, event):
#         print("connected", event)
#     async def websocket_receive(self,event):
#         print("receive", event)
#     async def websocket_disconnect(self, event):
#         print("disconnect", event)




