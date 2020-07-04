from channels.db import database_sync_to_async
import uuid as uuid_lib

# This decorator turns this function from a synchronous function into an async one
# we can call from our async consumers, that handles Django DBs correctly.
# For more, see http://channels.readthedocs.io/en/latest/topics/databases.html
from chat.exceptions import ClientError
from chat.models.chatModels import Chat, Message


@database_sync_to_async
def get_chat_or_error(chat_id, user):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    # Find the room they requested (by ID)
    try:
        chat = Chat.objects.get(uuid=chat_id)
    except Chat.DoesNotExist:
        raise ClientError("CHAT_INVALID")
    # Check permissions
    return chat


@database_sync_to_async
def get_user_chats_or_error(user):
    chat_ids = set()
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    # Find the room they requested (by ID)
    try:
        user_chats = Chat.objects.filter(self_user=user) | Chat.objects.filter(other_user=user)
        for chat in user_chats:
            chat_ids.add(str(chat.uuid))
    except Exception as e:
        raise ClientError("SERVER_CAN_NOT_GET_CHATS")
    return chat_ids


@database_sync_to_async
def save_chat_message(type, chat, sender, text, uuid):
    try:
        uuid_obj = uuid_lib.UUID(uuid)
        return Message.objects.create(type=type, chat=chat, sender=sender, text=text, uuid=uuid_obj)
    except Exception as e:
        print(e)
        raise ClientError("SERVER_CAN_NOT_SAVE_MESSAGE")
