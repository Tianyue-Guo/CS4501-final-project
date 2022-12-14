import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.http import HttpResponseRedirect

from asgiref.sync import sync_to_async
from .models import Message
from .models import World
from .rsa import decrypt
from threading import Thread
import concurrent.futures
import time

class ChatConsumer(AsyncWebsocketConsumer):



    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )




    # Receive message from web socket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']
        # print("original message: ", message)
        # await self.fetch_key(room)
        # key = asyncio.gather(self.fetch_key(room))
        # print(key)

            #print("ahhh return: ", return_value)


        with concurrent.futures.ThreadPoolExecutor() as executor1:

            future = executor1.submit(self.decryption, username, room, message)
            message = future.result()
        await self.save_message(username, room, message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

        with concurrent.futures.ThreadPoolExecutor() as executor2:
            future = executor2.submit(self.burn,username,room)


    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))


    @sync_to_async
    def save_message(self, username, room, message):
        Message.objects.create(username=username, room=room, content=message)

    def decryption(self, username, room, message):

        World_obj = World.objects.get(roomname = room, username=username)
        # print("obtained objects: ", World_obj)
        privatekey1 = getattr(World_obj, 'privatekey1')
        privatekey2 = getattr(World_obj, 'privatekey2')
        World_obj_security_level= getattr(World_obj, 'securitylevel')
        print("security level!!!: ", World_obj_security_level)
        if World_obj_security_level != "0":
        # print("Look at this", privatekey1, privatekey2)
            try:
                message = decrypt(message, (privatekey1, privatekey2))
            except:
                return message
        return message

    def burn(self, username, room):
        World_obj = World.objects.get(roomname = room, username=username)
        World_obj_security_level= getattr(World_obj, 'securitylevel')
        if World_obj_security_level != "2":
            return
        Message.objects.filter(username = username, room = room).update(content = "the message is burned!")
        print("the message is burned")



