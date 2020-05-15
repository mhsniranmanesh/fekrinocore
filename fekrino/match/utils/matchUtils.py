from chat.models.chatModels import Chat
from match.models.match import Match, Like, SuperLike


def check_and_match_users(self_user, other_user):
    try:
        if Like.objects.filter(user=other_user, like=self_user).count() > 0 or \
                SuperLike.objects.filter(user=other_user, superlike=self_user).count() > 0:
            if not check_if_users_have_been_matched(self_user, other_user):
                Match.objects.create(user=self_user, match=other_user)
                check_and_create_chat_for_users(self_user=self_user, other_user=other_user)
            return True
        return False

    except Exception as e:
        print(e)
        return False


def check_if_users_have_been_matched(user1, user2):
    try:
        if Match.objects.filter(user=user1, match=user2).count() > 0 or \
                Match.objects.filter(user=user2, match=user1).count() > 0:
            return True
        return False

    except Exception as e:
        print(e)
        return False


def check_and_create_chat_for_users(self_user, other_user):
    try:
        if Chat.objects.filter(self_user=self_user, other_user=other_user).count() > 0 or \
                Chat.objects.filter(self_user=other_user, other_user=self_user).count() > 0:
            pass
        else:
            Chat.objects.create(self_user=self_user, other_user=other_user)
    except Exception as e:
        print(e)