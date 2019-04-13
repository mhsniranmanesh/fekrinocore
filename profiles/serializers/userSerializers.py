from rest_framework import serializers

from profiles.models.user import User
from profiles.validators.userValidators import NameValidator, PhoneNumberValidator
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class UserEmailActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username')


class CreateUserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=30, required=True, validators=[PhoneNumberValidator()])
    class Meta:
        model = User
        fields = ('name', 'phone_number')


class UserGetPublicInfosSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'bio', 'date_joined', 'profile_picture', 'avatar',
                  'university', 'skills', 'client_projects', 'freelancer_projects', 'is_freelancer')


class UserGetInitialInfosSerializer(serializers.ModelSerializer):
    # skills = GetSkillsSerializer(many=True, read_only=True)
    # client_projects = GetProjectsSerializer(many=True, read_only=True)
    # freelancer_projects = GetProjectsSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'uuid', 'is_active', 'phone_number',
                  'is_email_verified', 'title', 'bio', 'date_joined', 'profile_picture', 'avatar', 'wish_coins',
                  'freelancer_rate', 'client_rate', 'freelancer_score', 'client_score', 'job', 'degree', 'university',
                  'skills', 'client_projects', 'freelancer_projects', 'balance', 'is_freelancer')


class UserUpdateInfosSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'bio', 'work', 'university')


class UserUpdateLocationSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    class Meta:
        model = User
        fields = ('name', 'latitude', 'longitude')