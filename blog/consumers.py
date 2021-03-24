from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Room, User, Message
from asgiref.sync import sync_to_async
import asyncio
import datetime
from django.utils import timezone, dateformat
from django.contrib.humanize.templatetags import humanize

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
        message = text_data_json['message']

        image = user.profile.image

        room = Room.objects.get(title=self.room_name)

        m = Message(room=room, user=user, content=message)
        m.save()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user_id': text_data_json["user_id"],
                'message': message,
                'image': str(image),
            }
        )

    async def chat_message(self, event):
        user_id = event["user_id"]
        message = event["message"]
        image = event["image"]

        now = humanize.naturaltime(datetime.datetime.now())

        await self.send(text_data=json.dumps({
            'user_id': user_id,
            'message': message,
            'image': str(image),
            'time': str(now),
        }))

    pass