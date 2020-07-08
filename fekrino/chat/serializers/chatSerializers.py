from rest_framework import serializers
from chat.models.chatModels import Chat, Message
from profiles.models.user import User
from profiles.serializers.profilePictureSerializers import GetProfilePictureSerializer


class ChatUsersSerializer(serializers.ModelSerializer):
    profile_pictures = GetProfilePictureSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields =['uuid', 'name', 'profile_pictures']


class ChatSerializer(serializers.ModelSerializer):
    self_user = ChatUsersSerializer()
    other_user = ChatUsersSerializer()

    class Meta:
        model = Chat
        fields = ('uuid', 'created_at', 'self_user', 'other_user')


class GetMessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(read_only=True, slug_field='uuid')
    
    class Meta:
        model = Message
        fields = ('uuid', 'created_at', 'type', 'replied_to', 'deleted_users', 'sender', 'text')


class GetChatMessagesPeriod(serializers.Serializer):
    message_id = serializers.UUIDField(required=True)
    count = serializers.IntegerField(required=True)