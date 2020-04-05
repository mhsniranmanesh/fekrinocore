from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from match.models.match import Like, Dislike, Match
from match.serializers.matchSerializers import LikeAndDislikeUserSerializer
from profiles.models.user import User


class LikeUserView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        pass
        # serializer = LikeAndDislikeUserSerializer(data=request.data)
        # if serializer.is_valid():
        #     try:
        #         is_matched = False
        #         user = request.user
        #         liked_user_uuid = serializer.validated_data.get('user_uuid')
        #         liked_user = User.objects.get(uuid=liked_user_uuid)
        #         Like.objects.create(user=user, like=liked_user)
        #         try:
        #             Like.objects.get(user=liked_user, like=user)
        #             Match.objects.create(user=user, match=liked_user)
        #
        #                 is_matched = True
        #             else:
        #                 is_matched = False
        #         except Exception as e:
        #             print(e)
        #             is_matched = False
        #         return Response(data={'is_matched': is_matched, 'data': serializer.data}, status=status.HTTP_200_OK)
        #
        #     except Exception as e:
        #         #Handle Exception
        #         return Response(data={'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DislikeUserView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = LikeAndDislikeUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = request.user
                disliked_user_uuid = serializer.validated_data.get('user_uuid')
                disliked_user = User.objects.get(uuid=disliked_user_uuid)
                Dislike.objects.create(user=user, dislike=disliked_user)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                #Handle Exception
                return Response(data={'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

