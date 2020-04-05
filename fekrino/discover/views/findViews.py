from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from discover.serializers.findSerializers import FindNearSerializer, NearUserSerializer
from profiles.models.user import User


class FindNearView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user = request.user
        serializer = FindNearSerializer(data=request.data)
        if serializer.is_valid():
            try:
                longitude = serializer.validated_data.get('longitude')
                latitude = serializer.validated_data.get('latitude')
                gender = serializer.validated_data.get('gender')
                limited_distance = int(serializer.validated_data.get('limited_distance'))
                user_location = Point(longitude, latitude)
                near_users = User.objects.filter(
                    gender = gender,
                    location__dwithin=(user_location, limited_distance / 111),
                ).filter(location__distance_lte=(user_location, D(km=limited_distance))
                         ).exclude(id=user.id).annotate(distance=Distance('location', user_location)
                                    ).order_by('distance')[0:10]
                near_users_serializer = NearUserSerializer(near_users, many=True)
                return Response(data=near_users_serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                # Handle Exception
                print(e)
                return Response(data={'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
