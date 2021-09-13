# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from datetime import datetime
from accounts.models import Account

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name =self.scope["url_route"]["kwargs"]["id"]
        #join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # accept connection
        await self.accept()
        print(f"room = {self.room_group_name}")

    async def disconnect(self, close_code):
        #leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message=text_data_json['message']
        #save message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type'   : 'chat_message',
                'message': message,
                'sender' : self.scope["user"].username,
                'photo'  : await get_picture(self.scope["user"].username)
            }
        )

    async def chat_message(self, event):
        """ Sends message to the corresponding client """
        await self.send(json.dumps(event))
        print((f'{event["sender"]}-> {self.scope["user"].username}'
               f' text_data={event["message"]}'))


@database_sync_to_async
def get_picture(username):
    photo = Account.objects.get(user__username = username).photo
    if photo:
        return photo.url
    else:
        return f'https://avatars.dicebear.com/api/initials/{username}.svg'

