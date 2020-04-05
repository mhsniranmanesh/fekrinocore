from rest_framework import serializers

from authentication.models.phoneActivation import PhoneActivationToken
from profiles.validators.userValidators import PhoneNumberValidator


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