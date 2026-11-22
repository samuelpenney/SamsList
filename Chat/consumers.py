from channels.generic.websocket import AsyncWebsocketConsumer
import json
class ChatConsumer(AsyncWebsocketConsumer):
    # ── CONNECT ──────────────────────────────────────────────────
    # Called when a browser opens the WebSocket connection
    async def connect(self):
        # Pull room name from the URL (captured by routing.py)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # Build a group label - everyone in "friends" room shares "chat_friends"
        self.group_name = f"chat_{self.room_name}"
        # Register this connection with the group via Redis
        # self.channel_name is a unique ID auto-assigned to THIS connection
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()  # without this → browser gets a 403 rejection
    # ── DISCONNECT ───────────────────────────────────────────────
    # Called when the tab closes or the network drops
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name  # removes only THIS connection, others stay
        )
    # ── RECEIVE ──────────────────────────────────────────────────
    # Called when a user sends a message from their browser
    async def receive(self, text_data):
        data    = json.loads(text_data)  # raw string → Python dict
        message = data['message']
        sender  = data['sender']
        # Broadcast to every connection in this group
        # 'type' tells Channels which method to call on each consumer
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type'   : 'chat_message',  # → calls chat_message() below
                'message': message,
                'sender' : sender,
            }
        )
    # ── CHAT_MESSAGE ─────────────────────────────────────────────
    # Called by group_send() on EACH connected user's consumer
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender' : event['sender'],
        }))