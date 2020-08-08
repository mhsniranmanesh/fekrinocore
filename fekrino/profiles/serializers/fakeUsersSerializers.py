from rest_framework import serializers
from profiles.models.profilePicture import ProfilePicture
from profiles.models.user import User



class FakeUserSerializer(serializers.ModelSerializer):
    profile_picture1 = serializers.ImageField(required=True)
    profile_picture2 = serializers.ImageField(required=False)
    profile_picture3 = serializers.ImageField(required=False)
    profile_picture4 = serializers.ImageField(required=False)
    profile_picture5 = serializers.ImageField(required=False)

    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)
    age = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ('name', 'bio', 'school', 'job', 'gender', 'age', 'city', 'latitude', 'longitude', 'profile_picture1',
                  'profile_picture2', 'profile_picture3', 'profile_picture4', 'profile_picture5')