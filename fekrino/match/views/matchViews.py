from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from match.models.match import Like, Dislike, SuperLike
from match.serializers.matchSerializers import LikeAndDislikeUserSerializer
from match.utils.matchUtils import check_and_match_users
from profiles.models.user import User


class LikeUserView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user = request.user
        serializer = LikeAndDislikeUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                liked_user_uuid = serializer.validated_data.get('user_uuid')
                liked_user = User.objects.get(uuid=liked_user_uuid)
                if user.id == liked_user.id:
                    return Response(data={'message': 'User can not like himself'}, status=status.HTTP_400_BAD_REQUEST)

                if Like.objects.filter(user=user, like=liked_user).count() == 0:
                    Like.objects.create(user=user, like=liked_user)

                is_matched = check_and_match_users(self_user=user, other_user=liked_user)

                return Response(data={'is_matched': is_matched, 'data': serializer.data}, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response(data={'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                #Handle Exception
                print(e)
                return Response(data={'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SuperLikeUserView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user = request.user
        serializer = LikeAndDislikeUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                superliked_user_uuid = serializer.validated_data.get('user_uuid')
                superliked_user = User.objects.get(uuid=superliked_user_uuid)
                if user.id == superliked_user.id:
                    return Response(data={'message': 'User can not super like himself'},
                                    status=status.HTTP_400_BAD_REQUEST)

                if SuperLike.objects.filter(user=user, superlike=superliked_user).count() == 0:
                    SuperLike.objects.create(user=user, superlike=superliked_user)

                is_matched = check_and_match_users(self_user=user, other_user=superliked_user)

                return Response(data={'is_matched': is_matched, 'data': serializer.data}, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response(data={'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                #Handle Exception
                return Response(data={'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DislikeUserView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = LikeAndDislikeUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = request.user
                disliked_user_uuid = serializer.validated_data.get('user_uuid')
                disliked_user = User.objects.get(uuid=disliked_user_uuid)
                if user.id == disliked_user.id:
                    return Response(data={'message': 'User can not dislike himself'},
                                    status=status.HTTP_400_BAD_REQUEST)

                if Dislike.objects.filter(user=user, dislike=disliked_user).count() == 0:
                    Dislike.objects.create(user=user, dislike=disliked_user)

                return Response(serializer.data, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response(data={'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                #Handle Exception
                return Response(data={'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

