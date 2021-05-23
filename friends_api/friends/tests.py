from django.test import TestCase, Client
from .factories import UserFactory
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import json
from .models import Friendship

class UserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test", email="test@mail.ru", password="VsfsfCmkd34!")
        token, created = Token.objects.get_or_create(user=self.user)

        self.client = Client()
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)

        self.users = UserFactory.build_batch(5)
        for user in self.users:
            user.save()

    def test_user_list(self):
        response = self.client.get('/v1/users/user_list/')
        self.assertTrue(response.status_code == 200)
        list_of_user = json.loads(response.content)
        self.assertEqual(len(list_of_user) - 1, len(self.users))

    def test_get_user(self):
        response = self.client.get('/v1/users/get_user/')
        self.assertTrue(response.status_code == 200)
        user = json.loads(response.content)
        self.assertEqual(user['id'], self.user.id)

    def test_get_user_by_id(self):
        response = self.client.get('/v1/users/get_user/', {'user_id': 2})
        self.assertTrue(response.status_code == 200)
        user = json.loads(response.content)
        self.assertEqual(user['id'], 2)

class FriendsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test",
            email="test@mail.ru",
            password="VsfsfCmkd34!")
        token, created = Token.objects.get_or_create(user=self.user)

        self.client = Client()
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)

        self.users = UserFactory.build_batch(5)
        for user in self.users:
            user.save()

        Friendship.objects.create(from_user=self.user, to_user=self.users[0])
        Friendship.objects.create(from_user=self.users[0], to_user=self.user)

        Friendship.objects.create(from_user=self.user, to_user=self.users[1])
        Friendship.objects.create(from_user=self.users[1], to_user=self.user)

        Friendship.objects.create(from_user=self.users[0], to_user=self.users[1])
        Friendship.objects.create(from_user=self.users[1], to_user=self.users[0])

        Friendship.objects.create(from_user=self.users[0], to_user=self.users[3])
        Friendship.objects.create(from_user=self.users[3], to_user=self.users[0])

        Friendship.objects.create(from_user=self.users[1], to_user=self.users[4])
        Friendship.objects.create(from_user=self.users[4], to_user=self.users[1])



    def test_add_friend(self):
        response = self.client.post('/v1/friends/add_friend/', {'user_id': self.users[4].id})
        self.assertTrue(response.status_code == 200)

        response = self.client.post('/v1/friends/add_friend/', {'user_id': self.user.id})
        self.assertTrue(response.status_code == 400)
        content = json.loads(response.content)
        self.assertEqual(content['message'], 'Users cannot be friend with themselves')

        response = self.client.post('/v1/friends/add_friend/', {'user_id': self.users[0].id})
        self.assertTrue(response.status_code == 400)
        content = json.loads(response.content)
        self.assertEqual(content['message'], 'Users are friends')

        response = self.client.post('/v1/friends/add_friend/', {'user_id': 100500})
        self.assertTrue(response.status_code == 400)
        content = json.loads(response.content)
        self.assertEqual(content['message'], 'Users does not exist')

    def test_delete_friend(self):
        response = self.client.delete('/v1/friends/delete_friend/',
                                      data=json.dumps({'user_id': self.users[0].id}),
                                      content_type='application/json')
        self.assertTrue(response.status_code == 200)

        response = self.client.delete('/v1/friends/delete_friend/',
                                      data=json.dumps({'user_id': self.user.id}),
                                      content_type='application/json')
        self.assertTrue(response.status_code == 400)
        content = json.loads(response.content)
        self.assertEqual(content['message'], 'friendship not found')

        response = self.client.delete('/v1/friends/delete_friend/',
                                      data=json.dumps({'user_id': 1100}),
                                      content_type='application/json')
        self.assertTrue(response.status_code == 400)
        content = json.loads(response.content)
        self.assertEqual(content['message'], 'Users does not exist')


    def test_get_friends(self):
        response = self.client.get('/v1/friends/get_friends/')
        self.assertTrue(response.status_code == 200)
        friends = json.loads(response.content)
        self.assertEqual(len(friends), 2)

        response = self.client.get('/v1/friends/get_friends/?user_id={}'.format(self.users[0].id))
        self.assertTrue(response.status_code == 200)
        friends = json.loads(response.content)
        self.assertEqual(len(friends), 3)

    def test_get_friends_of_friends(self):
        response = self.client.get('/v1/friends/get_friends_of_friends/')
        self.assertTrue(response.status_code == 200)
        friends = json.loads(response.content)
        self.assertEqual(len(friends), 2)



