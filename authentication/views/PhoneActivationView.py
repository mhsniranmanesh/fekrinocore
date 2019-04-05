from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models.phoneActivation import PhoneActivationToken
from authentication.serializers.PhoneActivationSerializer import GetPhoneTokenSerializer
from authentication.utils.PhoneActivationUtils import create_otp_token
from fekrino.utils.SmsUtils import send_sms


class GetPhoneTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetPhoneTokenSerializer(data=request.data)
        if serializer.is_valid():
            try:
                phone_number = serializer.validated_data['phone_number'],
                old_otp = PhoneActivationToken.objects.get(phone_number=phone_number, is_last=True)
                if old_otp.date_created - timezone.now() > timedelta(minutes=2):
                    pass

            except PhoneActivationToken.DoesNotExist:
                token = create_otp_token()
                new_otp = PhoneActivationToken.objects.create(phone_number=phone_number, is_last=True, token=token)
                send_sms(phone_number, new_otp)
                return Response(data={'message': 'token successfully sent'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(e)
                return Response(data={'message': 'something went wrong'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
