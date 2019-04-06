from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.models.profilePicture import ProfilePicture
from profiles.serializers.profilePictureSerializers import SetProfilePictureSerializer
from profiles.utils.profilePictureUtils import generate_resized_picture


class SetProfilePicture(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = SetProfilePictureSerializer(data=request.data)
        if serializer.is_valid():
            try:
                image = serializer.validated_data.get('image')
                priority = serializer.validated_data.get('priority')
                profile_picture = ProfilePicture(user=user, image=image, thumbnail=image, priority=priority)
                profile_picture.save()
                generate_resized_picture(profile_picture.image, 'image')
                generate_resized_picture(profile_picture.thumbnail, 'thumbnail')
                return Response(data={'message': 'Image created'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                # Handle Exception
                print(e)
                return Response(data={'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
