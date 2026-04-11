from django.test import TestCase

__all__ = ['CityTestCase']


class CityTestCase(TestCase):
    def test_city_view(self):
        response = self.client.get('/city/')
        self.assertEqual(response.status_code, 200)
