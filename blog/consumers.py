from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Room, User
from asgiref.sync import sync_to_async
import asyncio

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.user = self.scope["user"]
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        await self.channel_layer.group_add(
            self.room_group_name, 
            self.channel_name,
        )

        await self.accept()
    

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        user = User.objects.get(id=text_data_json["user_id"])
        image = user.profile.image.path

        message = text_data_json['message']
        username = self.scope["user"].username

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'image': image,
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        image = event["image"]

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'image': image,
        }))

    pass