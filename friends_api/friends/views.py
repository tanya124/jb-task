from rest_framework import viewsets, permissions, status
from .serializers import UserSerializer, FriendsSerializer
from .models import Friendship
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def user_list(self, request):
        """ Return a list of all users """
        serializer = UserSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def get_user(self, request):
        """
        If user_id parameter is given then
        return info for this user
        else return info for current user
        """
        try:
            user_id = request.GET.get('user_id')
            if user_id is None:
                user = self.queryset.get(username=request.user)
            else:
                user = self.queryset.get(id=user_id)

            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        except User.DoesNotExist:
            response_body = {'status': 'error', 'message': 'user does not exist'}
            return Response(response_body, status.HTTP_400_BAD_REQUEST)


class FriendsViewSet(viewsets.ModelViewSet):
    queryset = Friendship.objects.all()
    serializer_class = FriendsSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['POST'])
    def add_friend(self, request):
        """ Create friendship request """
        try:
            from_user = User.objects.get(username=request.user)
            to_user_id = request.data['user_id']
            to_user = User.objects.get(id=to_user_id)

            if from_user == to_user:
                response_body = {
                    'status': 'error',
                    'message': 'Users cannot be friend with themselves'
                }
                return Response(response_body, status.HTTP_400_BAD_REQUEST)

            if self.queryset.filter(from_user=from_user, to_user=to_user).exists():
                response_body = {'status': 'error', 'message': 'Users are friends'}
                return Response(response_body, status.HTTP_400_BAD_REQUEST)

            friendship, created1 = Friendship.objects.get_or_create(
                from_user=from_user, to_user=to_user
            )
            friendship, created2 = Friendship.objects.get_or_create(
                from_user=to_user, to_user=from_user
            )
            if created1 is False or created2 is False :
                response_body = {'status': 'error', 'message': 'Users are friends'}
                return Response(response_body, status.HTTP_400_BAD_REQUEST)

            response_body = {'status': 'success', 'message': 'friendship successfully created'}
            return Response(response_body, status.HTTP_200_OK)
        except User.DoesNotExist:
            response_body = {'status': 'error', 'message': 'Users does not exist'}
            return Response(response_body, status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['DELETE'])
    def delete_friend(self, request):
        """ Delete friendship request """
        try:
            from_user = User.objects.get(username=request.user)
            to_user_id = request.data['user_id']
            to_user = User.objects.get(id=to_user_id)

            qs = self.queryset.filter(
                Q(from_user=from_user, to_user=to_user) |
                Q(from_user=to_user, to_user=from_user)
            )
            if qs:
                qs.delete()
                response_body = {'status': 'success', 'message': 'friendship successfully deleted'}
                return Response(response_body, status.HTTP_200_OK)
            else:
                response_body = {'status': 'error', 'message': 'friendship not found'}
                return Response(response_body, status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            response_body = {'status': 'error', 'message': 'Users does not exist'}
            return Response(response_body, status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def get_friends(self, request):
        """
        if user_id parameter is given then
        return a list of friends for this user
        else return list of friends for current user
        """
        try:
            user_id = request.GET.get('user_id')
            if user_id is None:
                user = User.objects.get(username=request.user)
            else:
                user = User.objects.get(id=user_id)

            friends = Friendship.objects.filter(from_user=user)
            friends_serializer = FriendsSerializer(friends, many=True)
            return Response(friends_serializer.data)
        except User.DoesNotExist:
            response_body = {'status': 'error', 'message': 'Users does not exist'}
            return Response(response_body, status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def get_friends_of_friends(self, request):
        """
        Return a list of possible friends of the current user
        """
        user = User.objects.get(username=request.user)
        friends = self.queryset.values('to_user').filter(from_user=user)
        result_set_of_friends = self.queryset.none()
        for friend in friends:
            friend_id = friend['to_user']
            friends_of_friend = self.queryset.values('to_user')\
                    .filter(from_user=friend_id)\
                    .exclude(to_user=user)
            result_set_of_friends = result_set_of_friends.union(friends_of_friend)

        result_set_of_friends = result_set_of_friends.difference(friends)
        friends_id = [item['to_user'] for item in list(result_set_of_friends)]
        result = User.objects.filter(pk__in=friends_id)
        serializer = UserSerializer(result, many=True)
        return Response(serializer.data)


