from django.contrib.auth.base_user import BaseUserManager
from django.contrib.gis.geos import Point
from django.db import IntegrityError
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.models.user import User
from profiles.serializers.userSerializers import CreateUserSerializer, UserUpdateInfosSerializer, \
    UserUpdateLocationSerializer
from profiles.utils.userUtils import create_user_random_password


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    lookup_field = 'phone_number'

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User(
                    username=serializer.validated_data['phone_number'],
                    name = serializer.validated_data['name'],
                    phone_number = serializer.validated_data['phone_number'],
                )
                password = create_user_random_password()
                user.set_password(password)
                user.save()
                return Response(
                    data={'phone_number': user.phone_number,
                          'name': user.name,
                          'username': user.username,
                          'password': user.password
                          },
                    status=status.HTTP_200_OK
                )
            except IntegrityError:
                return Response(data={'phone_number': ['User with this phone number already exists']}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
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
                if 'name' in serializer.validated_data.keys():
                    user.name = serializer.validated_data.get('name')
                if 'bio' in serializer.validated_data.keys():
                    user.bio = serializer.validated_data.get('bio')
                if 'work' in serializer.validated_data.keys():
                    user.work = serializer.validated_data.get('work')
                if 'university' in serializer.validated_data.keys():
                    user.university = serializer.validated_data.get('university')
                if 'latitude' in serializer.validated_data.keys() and 'longitude' in serializer.validated_data.keys():
                    longitude = serializer.validated_data.get('longitude')
                    latitude = serializer.validated_data.get('latitude')
                    location = Point(longitude, latitude)
                    print(location)
                    user.location = location
                user.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(data={'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateLocationView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )


    def put(self, request):
        serializer = UserUpdateLocationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = request.user
                longitude = serializer.validated_data.get('longitude')
                latitude = serializer.validated_data.get('latitude')
                location = Point(longitude, latitude)
                user.location = location
                user.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                print(e)
                return Response(data={'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





