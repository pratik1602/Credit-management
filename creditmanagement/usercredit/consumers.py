from channels.generic.websocket import  AsyncWebsocketConsumer
from channels.exceptions import StopConsumer

import json

# First web socket connection try with following code but it not working so this is only for read.
# class TokenAuthConsumer(AsyncJsonWebsocketConsumer):
	
# 	async def connect(self):
# 		print(self.scope["user"].email)
# 		print('channel layer' , self.channel_layer)
# 		print('channel name' , self.channel_name)
# 		await self.channel_layer.group_add('Admin_notification',self.channel_name)
# 		await self.accept()
		
# 	async def disconnect(self, close_code):
# 		print("close code",close_code)
# 		await self.close()
# 		await self.channel_layer.group_discard('Admin_notification' , self.channel_name)
# 		raise StopConsumer()
	
	
# 	async def receive_json(self, content , **kwargs):
# 		print('Message from client to server' , content)
# 		print('Message from client to server' , content['message'])
# 		print('Message from client to server' , type(content['message']))
# 		print('Type of message from client to server' , type(content))
# 		# await self.send_json({'message': 'Message from server to client.'})

# 		await self.channel_layer.group_send('Admin_notification',{'type':'chat_message','message': 'Message from server to client.'})
	
    # async def chat_message(self , event):
    #     print('event......' , event)

    # async def receive_json(self, content , **kwargs):
    #     print('Message from client to server' , content)
    #     print('Type of message from client to server' , type(content))
    #     await self.send_json(
    #         {
    #             'message': 'Message from server to client.'
    #         }
    #     )

class AdminNotificationConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope['user'].email)
        print('channel layer :',self.channel_layer)
        print('channel name',self.channel_name)
        # Join room group
        await self.channel_layer.group_add("Admin_notification", self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard("Admin_notification", self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        print("message :",text_data)

        # Send message to room group
        await self.channel_layer.group_send(
            "Admin_notification", {"type": "chat.message", "message": "New user register."}
        )

    # Receive message from room group
    async def chat_message(self, event):
        print('event....' , event)
        id = event["_id"]
        f_name = event['f_name']
        l_name = event['l_name']
        print(id , f_name , l_name)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"id": id , 'first_name' : f_name , 'last_name' : l_name}))