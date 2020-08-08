from django.contrib.gis.geos import Point
from rest_framework import status
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.models.user import User
from profiles.serializers.userSerializers import UserUpdateInfosSerializer, UserUpdateLocationSerializer, \
    UserGetInitialInfosSerializer


class UserUpdateInfosView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )

    def put(self, request):
        serializer = UserUpdateInfosSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = request.user
                if 'name' in serializer.validated_data.keys():
                    user.name = serializer.validated_data.get('name')
                if 'bio' in serializer.validated_data.keys():
                    user.bio = serializer.validated_data.get('bio')
                if 'workplace' in serializer.validated_data.keys():
                    user.workplace = serializer.validated_data.get('workplace')
                if 'school' in serializer.validated_data.keys():
                    user.school = serializer.validated_data.get('school')
                if 'birthday' in serializer.validated_data.keys():
                    user.birthday = serializer.validated_data.get('birthday')
                if 'city' in serializer.validated_data.keys():
                    user.city = serializer.validated_data.get('city')
                if 'version' in serializer.validated_data.keys():
                    user.version = serializer.validated_data.get('version')
                if 'locale' in serializer.validated_data.keys():
                    user.locale = serializer.validated_data.get('locale')
                if 'job' in serializer.validated_data.keys():
                    user.job = serializer.validated_data.get('job')
                if 'gender' in serializer.validated_data.keys():
                    user.gender = serializer.validated_data.get('gender')
                if 'notification_token' in serializer.validated_data.keys():
                    user.notification_token = serializer.validated_data.get('notification_token')
                if 'platform' in serializer.validated_data.keys():
                    user.platform = serializer.validated_data.get('platform')
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


class UserGetInitialInfosView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        try:
            data = UserGetInitialInfosSerializer(user).data
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data={'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




