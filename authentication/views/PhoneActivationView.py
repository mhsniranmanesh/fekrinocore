from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models.phoneActivation import PhoneActivationToken
from authentication.serializers.PhoneActivationSerializer import GetPhoneTokenSerializer, VerifyPhoneTokenSerializer
from authentication.utils.PhoneActivationUtils import create_otp_token
from fekrino.utils.smsUtils import send_sms
from profiles.models.user import User
from profiles.utils.userUtils import create_user_random_password


class GetPhoneTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetPhoneTokenSerializer(data=request.data)
        if serializer.is_valid():
            try:
                phone_number = serializer.validated_data.get('phone_number')
                old_otp = PhoneActivationToken.objects.get(phone_number=phone_number, is_last=True)
                if timezone.now() - old_otp.date_created > timedelta(minutes=2):
                    token = create_otp_token()
                    new_otp = PhoneActivationToken.objects.create(phone_number=phone_number, is_last=True, token=token)
                    old_otp.is_last = False
                    old_otp.save()
                    send_sms(phone_number, new_otp.token)
                    return Response(data={'message': 'new token successfully sent'}, status=status.HTTP_201_CREATED)
                elif old_otp.is_again:
                    return Response(data={'message': 'token sent two times, try again after 2 minutes'},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    old_otp.is_again = True
                    old_otp.save()
                    send_sms(phone_number, old_otp.token)
                    return Response(data={'message': 'token sent again'}, status=status.HTTP_201_CREATED)
            except PhoneActivationToken.DoesNotExist:
                token = create_otp_token()
                otp = PhoneActivationToken.objects.create(phone_number=phone_number, is_last=True, token=token)
                send_sms(phone_number, otp.token)
                return Response(data={'message': 'token successfully sent'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(e)
                return Response(data={'message': 'something went wrong'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyPhoneTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = VerifyPhoneTokenSerializer(data=request.data)
        if serializer.is_valid():
            try:
                phone_number = serializer.validated_data.get('phone_number')
                token = serializer.validated_data.get('token')
                otp = PhoneActivationToken.objects.get(phone_number=phone_number, is_last=True)
                # print(otp.token)
                # print(token)

                if timezone.now() - otp.date_created > timedelta(minutes=2):
                    return Response(data={'message': 'token expired, get another'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    if otp.token == token:
                        try:
                            user = User.objects.get(username=phone_number)
                            password = create_user_random_password()
                            user.set_password(password)
                            user.save()
                            user_data = {
                                            'phone_number': user.phone_number,
                                            'name': user.name,
                                            'username': user.username,
                                            'password': password
                                        }
                            return Response(data=user_data, status=status.HTTP_200_OK)

                        except User.DoesNotExist:
                            user = User(
                                username=phone_number,
                                name='No name',
                                phone_number=phone_number,
                                is_active=True
                            )
                            password = create_user_random_password()
                            user.set_password(password)
                            user.save()
                            user_data = {
                                'phone_number': user.phone_number,
                                'name': user.name,
                                'username': user.username,
                                'password': password
                            }
                            return Response(data=user_data, status=status.HTTP_201_CREATED)
                        except Exception as e:
                            #Handle Exception
                            return Response(data={'message': 'something went wrong'},
                                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        return Response(data={'message': 'token is not correct'}, status=status.HTTP_400_BAD_REQUEST)
            except PhoneActivationToken.DoesNotExist:
                return Response(data={'message': 'no token obtained for this number'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response(data={'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
