from rest_framework import serializers

from match.models.match import Match


class LikeAndDislikeUserSerializer(serializers.Serializer):
    user_uuid = serializers.UUIDField()
