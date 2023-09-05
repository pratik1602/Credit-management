from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.exceptions import StopConsumer

import json

class TokenAuthConsumer(AsyncJsonWebsocketConsumer):
	
	async def connect(self):
		print(self.scope["user"].email)
		print('channel layer' , self.channel_layer)
		print('channel name' , self.channel_name)
		await self.channel_layer.group_add('Admin_notification',self.channel_name)
		await self.accept()
		
	async def disconnect(self, close_code):
		print("close code",close_code)
		await self.close()
		await self.channel_layer.group_discard('Admin_notification' , self.channel_layer)
		raise StopConsumer()
	
	
	async def receive_json(self, content , **kwargs):
		print('Message from client to server' , content)
		print('Message from client to server' , content['message'])
		print('Message from client to server' , type(content['message']))
		print('Type of message from client to server' , type(content))
		await self.send_json(
			{
				'message': 'Message from server to client.'
            }
        )
		# await self.channel_layer.group_send('Admin_notification',{'type':'chat_message','message': 'Message from server to client.'})
	
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