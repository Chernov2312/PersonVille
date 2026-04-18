__all__ = 'HomepageTestCase'
from django.test import TestCase


class HomepageTestCase(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
