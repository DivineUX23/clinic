import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .serializers import OrderSerializer
from .models import Order

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("orders", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("orders", self.channel_name)

    @sync_to_async
    def get_order_data(self, order_id):
        order = Order.objects.get(id=order_id)
        serializer = OrderSerializer(order)
        return serializer.data

    async def new_order(self, event):
        order_data = await self.get_order_data(event['order_id'])
        await self.send(text_data=json.dumps({
            'type': 'new_order',
            'order': order_data
        }))

    async def order_updated(self, event):
        order_data = await self.get_order_data(event['order_id'])
        await self.send(text_data=json.dumps({
            'type': 'order_updated',
            'order': order_data
        }))