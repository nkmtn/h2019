from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase


class PublicUserTests(APITestCase):

    # def test_create_account(self):
    #     url = "/api/user/create/"
    #     data = {'email': "email": "test@test.te", "password": "password"}
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    def test_login(self):
        url = "/api-token-auth/"
        response = self.client.post(url, {"email": "test@test.te", "password": "password"}, format='json')
        print(response.status_text)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)