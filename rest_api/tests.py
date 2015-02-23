# -*- coding : utf-8 -*-

from django.test import TestCase
# from django.utils import unittest
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from request_form.models import Performers, Requests
from django.contrib.auth.models import User

class PerformersAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.username = 'user'
        self.password = 'secret'
        self.user = User.objects.create_user(self.username,
                                             'mail@example.com',
                                             self.password)
        # self.user.is_staff = True
        # self.user.is_superuser = True
        # self.performer = Performers.objects.create(name="Alex")
        # Performers.objects.create(name="Alex")

    def test_not_authorizated_user(self):
        response = self.client.get('/api/performers/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # response = self.client.get('/api/request_list')
        # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # response = self.client.get('/api/request_list/1/')
        # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # response = self.client.post('/api/request_list/1/')
        # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_performer_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/performers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_performer(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/performers/', {'name': 'Alex'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get('/api/performers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Alex', response.content)

    def test_edit_performer(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/performers/', {'name': 'Alex'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.put('/api/performer_list/1/', {'name': 'Mark'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Mark', response.content)


    def test_delete_performer(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/performers/', {'name': 'Alex'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.delete('/api/performer_list/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # response = self.client.delete('/api/performer_list/1/')

        # self.assertRaises(Performers.DoesNotExist, Performers.objects.get, name="Vasia")
        # self.assertRaises(Performers.MultipleObjectsReturned, Performers.objects.get, name="Alex")
        # self.assertRaises(Performers.MultipleObjectsReturned, Performers.objects.get(name="Alex"))
        # self.assertEqual(self.performer.name, 'Alex')