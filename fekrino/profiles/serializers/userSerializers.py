from rest_framework import serializers

from match.models.match import Match, Like, SuperLike
from profiles.models.user import User
from profiles.serializers.profilePictureSerializers import GetProfilePictureSerializer


class UserGetPublicInfosSerializer(serializers.ModelSerializer):
    profile_pictures = GetProfilePictureSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('uuid', 'username', 'name', 'is_active', 'bio', 'birthday', 'gender', 'age', 'job', 'workplace',
                  'school', 'location', 'profile_pictures', 'city')


class GetMatchesSerializer(serializers.ModelSerializer):
    match = UserGetPublicInfosSerializer(read_only=True)

    class Meta:
        model = Match
        fields = ('created_at', 'match')


class GetBeenMatchesSerializer(serializers.ModelSerializer):
    user = UserGetPublicInfosSerializer(read_only=True)

    class Meta:
        model = Match
        fields = ('created_at', 'user')


class GetBeenLikesSerializer(serializers.ModelSerializer):
    user = UserGetPublicInfosSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('created_at', 'user')


class GetBeenSuperLikesSerializer(serializers.ModelSerializer):
    user = UserGetPublicInfosSerializer(read_only=True)

    class Meta:
        model = SuperLike
        fields = ('created_at', 'user')


class UserGetInitialInfosSerializer(serializers.ModelSerializer):
    profile_pictures = GetProfilePictureSerializer(many=True, read_only=True)
    user_matches = GetMatchesSerializer(many=True, read_only=True)
    user_been_matches = GetMatchesSerializer(many=True, read_only=True)
    user_been_likes = GetBeenLikesSerializer(many=True, read_only=True)
    user_been_super_likes = GetBeenSuperLikesSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('uuid', 'username', 'name', 'is_active', 'phone_number', 'bio', 'birthday', 'gender', 'age',
                  'date_joined', 'job', 'workplace', 'school', 'balance', 'rate', 'location', 'profile_pictures',
                  'version', 'locale', 'city', 'user_matches', 'user_been_matches', 'user_been_likes',
                  'user_been_super_likes')


class UserUpdateInfosSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'bio', 'workplace', 'school', 'birthday', 'city', 'version', 'locale', 'job')


class UserUpdateLocationSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    class Meta:
        model = User
        fields = ('latitude', 'longitude')
