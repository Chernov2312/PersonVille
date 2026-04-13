import http

from django.test import TestCase
from django.urls import reverse

__all__ = ['QuizzesTestCase']


class QuizzesTestCase(TestCase):
    def test_first_view(self):
        response = self.client.get(
            f"{reverse('quizzes:first')}?reset=1",
        )
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
