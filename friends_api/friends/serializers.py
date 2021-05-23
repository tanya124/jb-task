from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Friendship


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class FriendsSerializer(serializers.HyperlinkedModelSerializer):
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = ['to_user', 'created_date']
