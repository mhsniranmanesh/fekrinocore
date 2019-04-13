from rest_framework import serializers

from match.models.match import Like


class LikeAndDislikeUserSerializer(serializers.Serializer):
    user_uuid = serializers.UUIDField()
