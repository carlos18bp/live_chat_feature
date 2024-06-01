import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Conectarse a un grupo de WebSocket global
        await self.channel_layer.group_add(
            "global_chat",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Desconectarse del grupo global de WebSocket
        await self.channel_layer.group_discard(
            "global_chat",
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action', '')

        if action == "update_chat":
            # Enviar la actualización del chat a todos los clientes conectados
            await self.channel_layer.group_send(
                "global_chat",
                {
                    'type': 'chat_update'
                }
            )

    async def chat_update(self, event):
        await self.send(text_data=json.dumps({
            'action': 'update_chat'
        }))
