from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.models.chatModels import Chat, Message
from chat.serializers.chatSerializers import ChatSerializer, GetMessageSerializer, GetChatMessagesPeriod


class ChatListView(APIView):
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        try:
            chats = Chat.objects.filter(self_user=user) | Chat.objects.filter(other_user=user)
            chats_list = []
            for chat in chats:
                try:
                    last_message = Message.objects.filter(chat=chat).latest('id')
                except Message.DoesNotExist:
                    last_message = None
                last_message_data = GetMessageSerializer(last_message).data
                chat_data = ChatSerializer(chat).data
                if last_message:
                    chat_data['last_message'] = last_message_data
                chats_list.append(chat_data)
            return Response(chats_list, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(data={'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetChatMessagesView(APIView):
    serializer_class = GetChatMessagesPeriod
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user = request.user
        serializer = GetChatMessagesPeriod(data=request.data)
        if serializer.is_valid():
            try:
                message_uuid = serializer.validated_data['message_id']
                count = serializer.validated_data['count']
                if count > 50 or count < 2:
                    return Response(data={'message': 'Valid count should be between 2 and 50'},
                                    status=status.HTTP_400_BAD_REQUEST)
                base_message = Message.objects.get(uuid=message_uuid)

                if base_message.chat.self_user != user and base_message.chat.other_user != user:
                    return Response(data={'message': 'You do not have permission to this chat'},
                                    status=status.HTTP_400_BAD_REQUEST)
                messages = Message.objects.filter(created_at__lte=base_message.created_at,
                                                  chat=base_message.chat).order_by('-created_at')[:count]
                data = GetMessageSerializer(messages, many=True).data
                return Response(data, status=status.HTTP_200_OK)
            except Message.DoesNotExist:
                return Response(data={'message': 'message does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                print(e)
                return Response(data={'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ChatDetailView(RetrieveAPIView):
#     queryset = Chat.objects.all()
#     serializer_class = ChatSerializer
#     permission_classes = (AllowAny, )