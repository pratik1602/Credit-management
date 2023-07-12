# import json
# from channels.db import database_sync_to_async
# from asgiref.sync import sync_to_async
# from channels.consumer import SyncConsumer, AsyncConsumer
# from channels.exceptions import StopConsumer
# from usercredit.models import *
# from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from time import sleep # which is in seconds
import asyncio
from usercredit.models import *
from channels.db import database_sync_to_async
import json
from asgiref.sync import async_to_sync
from django.core.serializers import serialize   
from usercredit.api.serializers import *
from django.contrib.auth.models import AnonymousUser

#---------------- SYNC WEBSOCKET CONSUMER ---------------#

class MySyncWebsocketConsumer(WebsocketConsumer):
     
    def connect(self):
        print("Websocket connedted...")
        self.accept()
    
    def receive(self, text_data=None, bytes_data=None):
        print("Message received from client...", text_data)
        for i in range(10):
            self.send(text_data=str(i))
            sleep(1)


    def disconnect(self, close_code):
        print("Websocket disconnected....", close_code)


#------------- ASYNC WEBSOCKET CONSUMER ----------------#
from asgiref.sync import sync_to_async

class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    group_name = 'Notification-group'
    
    async def connect(self):
        if self.scope['user'].is_anonymous or not self.scope['user'].is_admin:
            print("if")
            print("Undefined user...!!!")
            await self.close()
        else:
            print("else")
            print("Websocket is connected...")
            print("user", self.scope['user'])
            print("channel layer", self.channel_layer)
            print("channel name", self.channel_name)
            # group_name = self.scope['user'].id
            print("group name", self.group_name)
            # print("group name 2", self.scope['url_route']['kwargs']['group_name']) 
            notifications = await database_sync_to_async(Notifications.objects.filter)(admin = self.scope['user']) 
            serialized_data = await sync_to_async(serialize)('json', notifications)       
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
            await self.send(json.dumps({
                'Status': 'Websocket connected...',
                'group_name': self.group_name,
            }))
            await self.send(text_data=serialized_data)

        
    async def receive(self, text_data=None, bytes_data=None):
        print("Message received from client...", text_data)
        
        notifications = await database_sync_to_async(Notifications.objects.filter)(admin = self.scope['user'])
        # print("noti", type(notifications))
        # list_notification = await sync_to_async(list)(notifications)
        serialized_data = await sync_to_async(serialize)('json', notifications)
        print("Serialized data", serialized_data)
        print("type Serialized data", type(serialized_data))
               
        # for i in serialized_data:
        #     print(i)
        await self.send(text_data=serialized_data)
        asyncio.sleep(1)
        
    async def send_queryset_data(self, event):
        print("hello from consumer")
        # queryset_data = await sync_to_async(serialize)('json', event['data'])
        # print("queryset data", type(queryset_data))
        # print("queryset data", queryset_data)
        await self.send(text_data=event['data'])

    # async def get_serialized_data(self):
    #     queryset = await sync_to_async(Notifications.objects.filter)(admin = self.scope['user'])()
    #     serialized_data = await sync_to_async(serialize)('json', queryset)
    #     return serialized_data  
    
    # async def send_notification(self, event):
    #     print("notification data", event)

    #     # await self.send(text_data= json.dumps({
    #     #     'msg': event['data']
    #     # })) 

    async def disconnect(self, close_code):
        print("hello")
        print("Websocket disconnected....", close_code)
        await self.send(text_data="User is undefined...")


#----------------- SYNC CONSUMER ---------------------#

# class MySyncConsumer(SyncConsumer):
#     def websocket_connect(self, event):
#         print("Websocket Connected...", event)
#         self.send({
#             'type': 'websocket.accept'
#         })
    
#     def websocket_receive(self, event):
#         print("Message Received from client....", event)
#         print("Printed Message is...", event["text"])
#         self.send({
#             'type' : 'websocket.send',
#             'text': 'Message sent to client'
#         })

#     def websocket_disconnect(self, event):
#         print("Websocket Disconnected...", event)
#         raise StopConsumer()


#-------------------- ASYNC CONSUMER -----------------#

# class MyAsyncConsumer(AsyncConsumer):
#     async def websocket_connect(self, event):
#         print("Websocket Connected...", event)
#         # token = get_user(self.scope['user'])
#         # print("token", token)
#         # user = token["user_id"]
#         # print("user", user)
    
#         await self.send({
#             'type': 'websocket.accept'
#         })
        
#     async def websocket_receive(self, event):
#         print("Message Received....", event)
#         print("Printed Message is...", event["text"])
#         # notification_objs = await database_sync_to_async(Notifications.objects.get)(admin = )
#         # print(type(notification_objs))
#         # print("noti objs", notification_objs)
#         # json_data =json.dumps(notification_objs)
#         # if self.scope['user'].is_admin:

#         notification_objs = await database_sync_to_async(Notifications.objects.all)()
#         list_data = await notification_objs
#         print(type(list_data))
#         # obj = json.dumps(notification_objs)
#         print(type(notification_objs))

#         # for data in notification_objs:
#         #     json_data = data

#         await self.send({
#             'type' : 'websocket.send',
#             'text': "abcd"
#         })
#         # else:
#         #     self.send({
#         #         'type':'websocket.send',
#         #         'text':{'msg':'Admin not found!!!'}
#         #     })

#     async def websocket_disconnect(self, event):
#         print("Websocket Disconnected...", event)
#         raise StopConsumer()



#----------------- DEMO ASYNC WEBSOCKET CONSUMER -------------------#


# from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from asgiref.sync import async_to_sync, sync_to_async
# from channels.layers import get_channel_layer
# from usercredit.models import *
# import json
# from channels.exceptions import StopConsumer


# @database_sync_to_async
# def create_notification(admin,typeof="task_created",is_seen=False):
#     notification_to_create=Notifications.objects.create(admin=admin,description=typeof)
#     print('I am here to help')
#     return (notification_to_create.admin.id,notification_to_create.description)

# class MyNotificationConsumer(AsyncWebsocketConsumer):
#     async def websocket_connect(self, event):
#         print("Websocket Connected...", event)
#         print('Am i finallyy here')
#         # print(self.scope['notification_id'].id)
#         await self.send({
#             'type': 'websocket.accept'
#         })

#         await self.send(json.dumps({
#             "type":"websocket.send",
#             "text":"hello Pratik !!"
#         }))

        
#     async def websocket_receive(self, event):
#         print("Message Received....", event)
#         print("Printed Message is...", event["text"])
#         await self.send({
#             'type' : 'websocket.send',
#             'text': 'Message sent to client'
#         })

#     async def websocket_disconnect(self, event):
#         print("Websocket Disconnected...", event)
#         raise StopConsumer()