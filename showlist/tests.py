from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from showlist import models
from showlist.api import serializers


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="newuser", password="NewUser===123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                           about="#1 Platform", web="https://www.netflix.com")

    def test_stream_platforms_create(self):
        data = {
            "name": "Netflix",
            "about": "#1 Streaming Platform in the World",
            "web": "https://netflix.com"
        }
        response = self.client.post(
            reverse('stream_platforms'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_stream_platforms_list(self):
        response = self.client.get(reverse('stream_platforms'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stream_platform_details(self):
        response = self.client.get(
            reverse('stream_platforms_details', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ShowListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="newuser", password="NewUser===123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                           about="#1 Platform", web="https://www.netflix.com")
        self.show = models.ShowList.objects.create(platform=self.stream, title="New Movie",
                                                   plot="New Movie", is_active=True)

    def test_show_list_create(self):
        data = {
            "platform": self.stream,
            "title": "New Movie",
            "plot": "New Story",
            "is_active": True
        }
        response = self.client.post(reverse('show_list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_show_list(self):
        response = self.client.get(reverse('show_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_list_details(self):
        response = self.client.get(
            reverse('show_details', args=(self.show.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.ShowList.objects.count(), 1)
        self.assertEqual(models.ShowList.objects.get().title, 'New Movie')


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="newuser", password="NewUser===123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                           about="#1 Platform", web="https://www.netflix.com")
        self.show = models.ShowList.objects.create(platform=self.stream, title="New Movie",
                                                   plot="New Movie", is_active=True)
        self.show_for_review_test = models.ShowList.objects.create(platform=self.stream, title="New Movie",
                                                                   plot="New Movie", is_active=True)
        self.review = models.Review.objects.create(author=self.user, rating=5, description="Nice Movie",
                                                   show_list=self.show_for_review_test, is_valid=True)

    def test_create_review(self):
        data = {
            "author": self.user,
            "rating": 5,
            "description": "Nice Movie!",
            "show_list": self.show,
            "is_active": True
        }

        response = self.client.post(
            reverse('create_review', args=(self.show.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)
        # self.assertEqual(models.Review.objects.get().rating, 5)

        response = self.client.post(
            reverse('create_review', args=(self.show.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauth(self):
        data = {
            "author": self.user,
            "rating": 5,
            "description": "Nice Movie!",
            "show_list": self.show,
            "is_active": True
        }

        # user = None - > means not authenticated
        self.client.force_authenticate(user=None)
        response = self.client.post(
            reverse('create_review', args=(self.show.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            "author": self.user,
            "rating": 4,
            "description": "Nice Movie! - updated",
            "show_list": self.show,
            "is_active": True
        }

        response = self.client.put(
            reverse('review_details', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(
            reverse('review_list', args=(self.show.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_details(self):
        response = self.client.get(
            reverse('review_details', args=(self.show.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_details_delete(self):
        response = self.client.delete(
            reverse('review_details', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
