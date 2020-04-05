from rest_framework import serializers

from fekrino.authentication.models.phoneActivation import PhoneActivationToken
from fekrino.profiles.models.user import User
from fekrino.profiles.validators.userValidators import PhoneNumberValidator


class GetPhoneTokenSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[PhoneNumberValidator()])

    class Meta:
        model = PhoneActivationToken
        fields = ['phone_number']


class VerifyPhoneTokenSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[PhoneNumberValidator()])

    class Meta:
        model = PhoneActivationToken
        fields = ['phone_number', 'token']