from channels.db import database_sync_to_async
from django.conf import settings

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from chat.exceptions import ClientError
from chat.models.chatModels import Message
from chat.utils.chatUtils import get_chat_or_error, get_user_chats_or_error, save_chat_message


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    This chat consumer handles websocket connections for chat clients.
    It uses AsyncJsonWebsocketConsumer, which means all the handling functions
    must be async functions, and any sync work (like ORM access) has to be
    behind database_sync_to_async or sync_to_async. For more, read
    http://channels.readthedocs.io/en/latest/topics/consumers.html
    """

    ##### WebSocket event handlers

    async def connect(self):
        #print("CONNECTTTTT")
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        # Are they logged in?
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()
        else:
            # Accept the connection
            await self.accept()
            self.chat_ids = set()
            user_chat_ids = await get_user_chats_or_error(self.scope["user"])
            for chat_id in user_chat_ids:
                await self.join_chat(chat_id)
        # Store which chats the user has joined on this connection


    async def receive_json(self, content):
        #print("RECIEVE JSONNNN")
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        # Messages will have a "command" key we can switch on
        command = content.get("command", None)
        try:
            if command == "send":
                await self.send_chat(content["chat_id"], content["message_type"], content["text"], content["uuid"])
            if command == "status":
                await self.set_status(content["chat_id"], content["status"])
        except ClientError as e:
            # Catch any errors and send it back
            await self.send_json({"error": e.code})


    async def disconnect(self, code):
        #print("DISCONNECTTTT")
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave all the rooms we are still in
        if self.chat_ids:
            active_chat_ids = self.chat_ids.copy()
            for chat_id in active_chat_ids:
                try:
                    await self.leave_chat(chat_id)
                except ClientError:
                    pass

    ##### Command helper methods called by receive_json

    async def join_chat(self, chat_id):
        #print("JOIN CHATTT")
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        self.chat_ids.add(chat_id)
        # Add them to the group so they get room messages
        await self.channel_layer.group_add(
            chat_id,
            self.channel_name,
        )


    async def leave_chat(self, chat_id):
        #print("LEAVE CHATTTT")
        self.chat_ids.discard(chat_id)
        # Remove them from the group so they no longer get room messages
        await self.channel_layer.group_discard(
            chat_id,
            self.channel_name,
        )

    async def send_chat(self, chat_id, message_type, text, uuid):
        #print("SEND_CHATTTT")
        """
        Called by receive_json when someone sends a message to a chat.
        """
        # Check they are in this room
        if chat_id not in self.chat_ids:
            raise ClientError("CHAT_ACCESS_DENIED")
        # Get the room and send to the group about it
        await self.channel_layer.group_send(
            chat_id,
            {
                "type": "chat.message",
                "chat_id": chat_id,
                "sender": str(self.scope["user"].uuid),
                "message_type": message_type,
                "text": text,
                "uuid": uuid,
            }
        )
        chat = await get_chat_or_error(chat_id, self.scope["user"])
        await save_chat_message(chat=chat, type=message_type, sender=self.scope["user"], text=text, uuid=uuid)


    async def set_status(self, chat_id, status):
        #print("SET_STATUSSSS")
        """
        Called by receive_json when someone sends a message to a chat.
        """
        # Check they are in this room
        if chat_id not in self.chat_ids:
            raise ClientError("ACCESS_DENIED")
        # Get the room and send to the group about it
        await self.channel_layer.group_send(
            chat_id,
            {
                "type": "chat.status",
                "chat_id": chat_id,
                "sender": str(self.scope["user"].uuid),
                "status": status
            }
        )

    ##### Handlers for messages sent over the channel layer

    # These helper methods are named by the types we send - so chat.message becomes chat_message
    async def chat_message(self, event):
        #print("CHAT MESSAGEEEE")
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "msg_type": settings.CMD_TYPE_MESSAGE,
                "chat_id": event["chat_id"],
                "sender": event["sender"],
                "message_type": event["message_type"],
                "text": event["text"],
                "uuid": event["uuid"]
            },
        )

    async def chat_status(self, event):
        #print("CHAT STATUSSSS")
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "msg_type": settings.CMD_TYPE_STATUS,
                "chat_id": event["chat_id"],
                "sender": event["sender"],
                "status": event["status"]
            },
        )