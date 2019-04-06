from rest_framework import serializers

from profiles.models.profilePicture import ProfilePicture


class SetProfilePictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfilePicture
        fields = ['image', 'priority']