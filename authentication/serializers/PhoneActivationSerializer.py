from rest_framework import serializers
from profiles.models.user import User
from profiles.validators.userValidators import PhoneNumberValidator


class GetPhoneTokenSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        validators=[PhoneNumberValidator()])

    class Meta:
        model = User
        fields = ['phone_number']