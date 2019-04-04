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
    name = serializers.CharField(max_length=50, required=True, validators=[NameValidator()])
    phone_number = serializers.CharField(max_length=30, required=True, validators=[PhoneNumberValidator()])
    password = serializers.CharField(min_length=8, max_length=128, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'phone_number', 'is_freelancer')

    def create(self, validated_data):
        user = User.objects.create(
           username=validated_data['username'],
           name=validated_data['name'],
           phone_number=validated_data['phone_number'],
        )
        user.set_password(validated_data['password'])
        user.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.uuid))
        user.send_sms(uid, token)
        return user


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
        fields = ('title', 'bio', 'job', 'degree', 'university', 'profile_picture')


