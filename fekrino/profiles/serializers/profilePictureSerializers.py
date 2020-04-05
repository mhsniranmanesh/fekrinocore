from rest_framework import serializers

from profiles.models.profilePicture import ProfilePicture


class SetProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePicture
        fields = ['image', 'priority']


class DeleteProfilePictureSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()

    class Meta:
        model = ProfilePicture
        fields = ['uuid']


class SetProfilePicturePrioritySerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()
    priority = serializers.IntegerField(min_value=1, max_value=6)

    class Meta:
        model = ProfilePicture
        fields = ['uuid', 'priority']


class GetProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePicture
        fields = ['uuid', 'image', 'thumbnail', 'priority']