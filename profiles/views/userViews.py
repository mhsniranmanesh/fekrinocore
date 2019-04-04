from django.db import IntegrityError
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.models.user import User
from profiles.serializers.userSerializers import CreateUserSerializer, UserUpdateInfosSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    lookup_field = 'phone_number'

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.create(
                    username=serializer.validated_data['phone_number'],
                    name = serializer.validated_data['name'],
                    phone_number = serializer.validated_data['phone_number']
                )
                return Response(data={'phone_number': user.phone_number, 'name': user.name}, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response(data={'phone_number': ['User with this phone number already exists']}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response(data={'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateInfosView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )


    def post(self, request):
        serializer = UserUpdateInfosSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = request.user
                if 'bio' in serializer.validated_data.keys():
                    user.bio = serializer.validated_data['bio']
                if 'job' in serializer.validated_data.keys():
                    user.job = serializer.validated_data['job']
                if 'university' in serializer.validated_data.keys():
                    user.university = serializer.validated_data['university']
                user.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(data={'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
