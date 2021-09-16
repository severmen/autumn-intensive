import json
import datetime
import time
import re
from django.template import loader

import channels
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from project.settings import mongoDB_services
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.contenttypes.models import ContentType
from channels.db import database_sync_to_async
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        '''
        функция помимо фиксирует пользователя в
        '''
        # фиксируем пользователи и имя канала
        index = {
            "nickname": self.scope['url_route']['kwargs']['nickname'],
            "channel_name": self.channel_name
        }
        mongoDB_services.insert_one(index)
        self.post_group_name = "chat"

        await self.channel_layer.group_add(
            self.post_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        mongoDB_services.delete_one({"channel_name": self.channel_name})
        await self.channel_layer.discard(
            self.post_group_name,
            self.channel_name
        )

    # Получить сообщение от WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        new_massage = await self.create_new_message(text_data_json)
        message = {
            "nickname": new_massage.nikname,
            "message": new_massage.message,
            "date_time": {"date": str(new_massage.data_time.day) + "."
                                  + str(new_massage.data_time.month) + "."
                                  + str(new_massage.data_time.year),
                          "time": str(new_massage.data_time.hour) + ":"
                                  + str(new_massage.data_time.minute)
                          }
        }

        await self.channel_layer.group_send(
            self.post_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

        # Receive message from room group

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def create_new_message(self, data):
        def check_length(message):
            message = loader.render_to_string('chat/escaping.html', {"text":message})
            result = ""
            for word in message.split(" "):
                if len(word) > 23:
                    result += " "
                    count = 0
                    for character in list(word):
                        count += 1
                        result += character
                        if count == 23:
                            count = 0
                            result += "\r\n"
                else:
                    result += " "+word
            return result

        new_message = Message(
            nikname=data.get('nickname'),
            message=check_length(data.get('message'))
        )
        new_message.save()
        return new_message



class Time(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_group_name = "time"

        await self.channel_layer.group_add(
            self.post_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.discard(
            self.post_group_name,
            self.channel_name
        )

    # Получить сообщение от WebSocket


    async def receive(self, text_data):
        def date_time_dict():
            def get_day_of_week():
                week_name = [
                    'Mon', 'Tue',
                    'Wed', 'Thu',
                    'Fri', 'Sat',
                ]
                return week_name[datetime.datetime.today().weekday()]

            time_now = datetime.datetime.now()
            return {
                "day_of_week": get_day_of_week(),
                "time": str(time_now.hour) + ":" + str(time_now.minute)
            }
        await self.channel_layer.group_send(
        self.post_group_name, {
            'type': 'chat_time',
            'date_time': date_time_dict()
            }
        )

    async def chat_time(self, event):
        date_time = event['date_time']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'date_time': date_time
        }))
