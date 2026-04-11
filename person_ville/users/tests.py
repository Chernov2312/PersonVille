from django.test import TestCase

__all__ = ['UsersTestCase']


class UsersTestCase(TestCase):
    def test_users(self):
        self.assertEqual(1, 1)
