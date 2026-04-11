from django.test import TestCase

__all__ = ['HomepageTestCase']


class HomepageTestCase(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
