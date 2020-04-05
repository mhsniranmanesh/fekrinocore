from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.models.profilePicture import ProfilePicture
from profiles.serializers.profilePictureSerializers import SetProfilePictureSerializer, DeleteProfilePictureSerializer, \
    GetProfilePictureSerializer, SetProfilePicturePrioritySerializer
from profiles.utils.profilePictureUtils import generate_resized_picture


class ProfilePictureView(APIView):
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
                profile_picture_data = GetProfilePictureSerializer(profile_picture).data
                return Response(data={'profile_picture': profile_picture_data}, status=status.HTTP_201_CREATED)
            except Exception as e:
                # Handle Exception
                return Response(data={'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        serializer = DeleteProfilePictureSerializer(data=request.data)
        if serializer.is_valid():
            try:
                uuid = serializer.validated_data.get('uuid')
                image = ProfilePicture.objects.get(uuid=uuid)
                image.delete()
                for profile_picture in user.profile_pictures.filter(priority__gt=image.priority):
                    profile_picture.priority = profile_picture.priority - 1
                    profile_picture.save()
                return Response(data={'message': 'image deleted successfully'}, status=status.HTTP_200_OK)
            except ProfilePicture.DoesNotExist:
                return Response(data={'message': 'image does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                # Handle Exception
                return Response(data={'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetProfilePicturePriorityView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = SetProfilePicturePrioritySerializer(data=request.data)
        if serializer.is_valid():
            try:
                uuid = serializer.validated_data.get('uuid')
                priority = serializer.validated_data.get('priority')
                profile_picture = ProfilePicture.objects.get(uuid=uuid)
                profile_picture.priority = priority
                profile_picture.save()
                profile_picture_data = GetProfilePictureSerializer(profile_picture).data
                return Response(data={'profile_picture': profile_picture_data}, status=status.HTTP_200_OK)

            except ProfilePicture.DoesNotExist:
                return Response(data={'message': 'image does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                # Handle Exception
                print(e)
                return Response(data={'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
