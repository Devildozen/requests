# -*- coding : utf-8 -*-

import random

# from django.test import TestCase
# from django.utils import unittest
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from request_form.models import Performers, Requests
from django.contrib.auth.models import User


class Urls(object):
    performers = '/api/performers/'
    performer_list = '/api/performer_list/'
    request_list = '/api/request_list'


def r():
    return str(random.randint(1, 9))


class PermissionsCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.username = 'user'
        self.password = 'secret'
        self.user = User.objects.create_user(self.username, 'mail@example.com',
                                             self.password)

    def test_not_authorized_user(self):
        response = self.client.get(Urls.performers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get(Urls.request_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get('%s/1/' % Urls.request_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post('%s/1/' % Urls.request_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PerformersAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.username = 'user'
        self.password = 'secret'
        self.user = User.objects.create_user(self.username, 'mail@example.com',
                                             self.password)
        Performers.objects.create(name='Nick')
        self.client.force_authenticate(user=self.user)

    def test_get_performer_list(self):
        response = self.client.get(Urls.performers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_performer(self):
        response = self.client.post(Urls.performers, {'name': 'Alex'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(Urls.performers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Alex', response.content)

    def test_edit_performer(self):
        response = self.client.put('%s1/' % Urls.performer_list,
                                   {'name': 'Mark'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Mark', response.content)

    def test_delete_performer(self):
        response = self.client.delete('%s1/' % Urls.performer_list)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class RequestAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = 'user'
        self.password = 'secret'
        self.user = User.objects.create_user(self.username, 'mail@example.com',
                                             self.password)
        self.client.force_authenticate(user=self.user)

        Performers.objects.create(name='Alex')
        Performers.objects.create(name='Mark')

        self.requests = []
        for i in range(5):
            request = Requests.objects.create(
                in_number=str(i) * 5,
                out_number=str(i+1) * 5,
                text='some text',
                filling_date='2015-02-04',
                performance_date='2015-02-04',
                applicant='Applicant-' + str(i),
                performer=Performers.objects.get(id=i % 2 + 1)
            )
            self.requests.append(request)
        req = self.requests[1]
        self.json_data = {
            'in_number': req.in_number,
            'out_number': req.out_number,
            'text': req.text,
            'filling_date': req.filling_date,
            'performance_date': req.performance_date,
            'applicant': req.applicant,
            'performer': 1,
        }

    def test_get_request_list(self):
        response = self.client.get(Urls.request_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_request(self):
        self.json_data['in_number'] = '123'
        self.json_data['out_number'] = '321'
        response = self.client.post(Urls.request_list, self.json_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('123', response.content)

    def test_edit_request(self):
        self.json_data['in_number'] = '123'
        self.json_data['out_number'] = '321'
        response = self.client.put('%s/4/' % Urls.request_list, self.json_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('%s/4/' % Urls.request_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('123', response.content)

    def test_delete_request(self):
        response = self.client.delete('%s/4/' %
                                      Urls.request_list, self.json_data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_exist_request(self):
        response = self.client.post(Urls.request_list, self.json_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictContainsSubset(
            {'in_number': ['This field must be unique.']},
            response.data
        )
        self.assertDictContainsSubset(
            {'out_number': ['This field must be unique.']}, response.data)

    def test_edit_exist_request(self):
        response = self.client.put('%s/3/' % Urls.request_list, self.json_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictContainsSubset(
            {'in_number': ['This field must be unique.']}, response.data)
        self.assertDictContainsSubset(
            {'out_number': ['This field must be unique.']}, response.data)


class RequestFilterOrderingTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.username = 'user'
        self.password = 'secret'
        self.user = User.objects.create_user(self.username, 'mail@example.com',
                                             self.password)
        self.client.force_authenticate(user=self.user)

        Performers.objects.create(name='Alex')
        Performers.objects.create(name='Mark')

        for i in range(5):
            Requests.objects.create(
                in_number=str(i) * 5,
                out_number=str(i+1) * 5,
                text='some text',
                filling_date='201%s-0%s-0%s' % (r(), r(), r()),
                performance_date='201%s-0%s-0%s' % (r(), r(), r()),
                # filling_date='201'+r()+'-0'+r()+'-0'+r(),
                # performance_date='201'+r()+'-0'+r()+'-0'+r(),
                applicant='Applicant-%s' % r(),
                performer=Performers.objects.get(id=i % 2 + 1)
            )
        self.filter_fields = [
            'in_number',
            'out_number',
            'text',
            'filling_date',
            'performance_date',
            'applicant',
            'performer',
        ]
        self.ordering_fields = (
            'id',
            'in_number',
            'out_number',
            'filling_date',
            'performance_date',
            'text',
            'applicant',
            'performer__name',
            '-id',
            '-in_number',
            '-out_number',
            '-filling_date',
            '-performance_date',
            '-text',
            '-applicant',
            '-performer__name',
        )

    def test_order(self):
        for field in self.ordering_fields:
            query = (Requests.objects.all().
                     order_by(field).
                     values_list('id', flat=True))
            response = self.client.get('%s?ordering=%s' %
                                       (Urls.request_list, field))
            for i, q in enumerate(query):
                self.assertEqual(q, response.data['results'][i]['id'])

    def test_filtering(self):
        for field in self.filter_fields:
            query = Requests.objects.select_related('performer').get(id=1)#.values()
            values = query.__dict__[field]
            # query = Requests.objects.get(
            #     id=random.randint(1, Requests.objects.all().count())
            # ).values()
            # values = {
            #     'in_number': query.in_number,
            #     'out_number': query.out_number,
            #     'text': query.text,
            #     'filling_date': query.filling_date,
            #     'performance_date': query.performance_date,
            #     'applicant': query.applicant,
            #     'performer': query.performer,
            # }
            query = (Requests.objects.all().
                     filter(**{field: values}).
                     # filter(**{field: values[field]}).
                     values_list('id', flat=True))
            response = self.client.get('%s?%s=%s' %
                                       (Urls.request_list, field, values))
                                       # (Urls.request_list, field, values[field]))
            self.assertEqual(len(query), len(response.data['results']))
            for rec in response.data['results']:
                self.assertIn(rec['id'], query)