import http

from django.test import TestCase
from django.urls import reverse

__all__ = ['CityTestCase']


class CityTestCase(TestCase):
    def test_city_view(self):
        response = self.client.get(reverse('city:city'))
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
