from rest_framework import serializers


class LikeAndDislikeUserSerializer(serializers.Serializer):
    user_uuid = serializers.UUIDField()
