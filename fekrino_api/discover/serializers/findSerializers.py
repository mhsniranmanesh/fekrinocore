from rest_framework import serializers
from profiles.models.user import User
from profiles.serializers.profilePictureSerializers import GetProfilePictureSerializer


class FindNearSerializer(serializers.Serializer):
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    gender = serializers.CharField()
    limited_distance = serializers.IntegerField()


class NearUserSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()
    profile_pictures = GetProfilePictureSerializer(many=True)

    def get_distance(self, obj):
        return int(obj.distance.m)

    class Meta:
        model = User
        fields = ('uuid', 'name', 'profile_pictures','distance')