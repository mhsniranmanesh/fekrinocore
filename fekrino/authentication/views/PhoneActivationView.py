from datetime import timedelta
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

# import logging

#logger = logging.getlogger('authentication')


class GetPhoneTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        send_sms('+989102334456', '123456', 'fectogram')
        return Response(data={'message': 'token successfully sent'}, status=status.HTTP_201_CREATED)
        # serializer = GetPhoneTokenSerializer(data=request.data)
        # pattern = 'fekrino'
        # if request.query_params.__contains__('pattern'):
        #     pattern = request.query_params['pattern']
        #
        # if serializer.is_valid():
        #     try:
        #         phone_number = serializer.validated_data.get('phone_number')
        #         old_otps = PhoneActivationToken.objects.filter(phone_number=phone_number, is_last=True)
        #         old_otp = old_otps.latest('id')
        #         if timezone.now() - old_otp.date_created > timedelta(minutes=2):
        #             for o_otp in old_otps:
        #                 o_otp.is_last = False
        #                 o_otp.save()
        #             token = create_otp_token()
        #             new_otp = PhoneActivationToken.objects.create(phone_number=phone_number, is_last=True, token=token)
        #             print("BEFORE SEND SMS")
        #             send_sms(phone_number, new_otp.token, pattern)
        #             #logger.info("OTP successfully sent")
        #             return Response(data={'message': 'new token successfully sent'}, status=status.HTTP_201_CREATED)
        #         elif old_otp.is_again:
        #             #logger.warning("OTP sent two times, waiting 2 mins")
        #             return Response(data={'message': 'token sent two times, try again after 2 minutes'},
        #                             status=status.HTTP_400_BAD_REQUEST)
        #         else:
        #             old_otp.is_again = True
        #             old_otp.save()
        #             send_sms(phone_number, old_otp.token, pattern)
        #             #logger.info("OTP successfully sent again")
        #             return Response(data={'message': 'token sent again'}, status=status.HTTP_201_CREATED)
        #     except PhoneActivationToken.DoesNotExist:
        #         token = create_otp_token()
        #         otp = PhoneActivationToken.objects.create(phone_number=phone_number, is_last=True, token=token)
        #         send_sms(phone_number, otp.token, pattern)
        #         #logger.info("OTP successfully sent")
        #         return Response(data={'message': 'token successfully sent'}, status=status.HTTP_201_CREATED)
        #     except Exception as e:
        #         #logger.error("exception during OTP : %s", e)
        #         return Response(data={'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # #logger.warning("OTP serializer error %s", serializer.errors)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyPhoneTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = VerifyPhoneTokenSerializer(data=request.data)
        if serializer.is_valid():
            try:
                phone_number = serializer.validated_data.get('phone_number')
                token = serializer.validated_data.get('token')
                otp = PhoneActivationToken.objects.filter(phone_number=phone_number, is_last=True).latest('id')

                if timezone.now() - otp.date_created > timedelta(minutes=2):
                    #logger.warning("token expired")
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
                                            'password': password,
                                            'is_new_user': False
                                        }
                            #logger.info("account created")
                            return Response(data=user_data, status=status.HTTP_200_OK)

                        except User.DoesNotExist:
                            user = User(
                                username=phone_number,
                                name='No name',
                                phone_number=phone_number,
                                is_active=True,
                            )
                            password = create_user_random_password()
                            user.set_password(password)
                            user.save()
                            user_data = {
                                'phone_number': user.phone_number,
                                'name': user.name,
                                'username': user.username,
                                'password': password,
                                'is_new_user': True
                            }
                            #logger.info("account created")
                            return Response(data=user_data, status=status.HTTP_201_CREATED)
                        except Exception as e:
                            #logger.error("Exceptions during varifying OTP: %s", e)
                            return Response(data={'message': 'something went wrong'},
                                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        #logger.warning("OTP is not correct")
                        return Response(data={'message': 'token is not correct'}, status=status.HTTP_400_BAD_REQUEST)
            except PhoneActivationToken.DoesNotExist:
                #logger.warning("no token obtained for this number")
                return Response(data={'message': 'no token obtained for this number'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                #logger.error("Excetion During varifying OTP: %s", e)
                return Response(data={'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #logger.warning("OTP verify serializer error")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
