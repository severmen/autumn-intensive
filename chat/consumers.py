import json
import datetime

from django.template import loader
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from project.settings import mongoDB_services
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    '''
    организовывает WebSocket соединие для обмена сообщениями
    '''
    async def connect(self):
        '''
        функция помимо соединение фиксирует пользователя в mongo чтобы дв пользовтеля
         не смоглиавтоизовать в системе
        '''
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
        #удалеться пользователя из mongo
        mongoDB_services.delete_one({"channel_name": self.channel_name})
        await self.channel_layer.discard(
            self.post_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        '''
        получаеть собщение от пользователя фиксирует все данные в БД
        и отпрвляет всем подключённым пользователям
        '''
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



    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def create_new_message(self, data):
        '''
        фиксирует сообщение в БД, проводя проверка на XSS
        и чрезмернуню длину сообщения
        '''
        def check_length_and_XSS(message):
            '''
            проводит проверку на XSS
            и чрезмернуню длину сообщения в 23 и больше символов
            '''
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
            message=check_length_and_XSS(data.get('message'))
        )
        new_message.save()
        return new_message

class Time(AsyncWebsocketConsumer):
    '''
        организовывает WebSocket соединие синхронизации врмени с сервером
    '''
    async def connect(self):
        '''
        подключениен к каналу
        '''
        self.post_group_name = "time"

        await self.channel_layer.group_add(
            self.post_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        '''
        отключние от канала
        '''
        await self.channel_layer.discard(
            self.post_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        def date_time_dict():
            '''
            отправлет клиенту текущий день недели время и дату
            '''
            def get_day_of_week():
                '''
                Возврощает в сокращённом формате день денели
                '''
                week_name = [
                    'Mon', 'Tue',
                    'Wed', 'Thu',
                    'Fri', 'Sat',
                ]
                return week_name[datetime.datetime.today().weekday()]

            def push_zero(number):
                '''
                добавлят ноль к времен чтобы выглядило красиво
                '''
                if number < 10:
                    return "0"+str(number)
                return number

            time_now = datetime.datetime.now()
            return {
                "day_of_week": get_day_of_week(),
                "time": str(push_zero(time_now.hour)) + ":" + str(push_zero(time_now.minute))
            }
        await self.channel_layer.group_send(
        self.post_group_name, {
            'type': 'chat_time',
            'date_time': date_time_dict()
            }
        )

    async def chat_time(self, event):
        date_time = event['date_time']
        await self.send(text_data=json.dumps({
            'date_time': date_time
        }))
