import http

from django.test import TestCase
from django.urls import reverse

__all__ = ['QuizzesTestCase']


class QuizzesTestCase(TestCase):
    def test_first_view(self):
        response = self.client.post(
            reverse('quizzes:first', kwargs={'number': 1}),
            data={'answer': 'answer1'},
        )
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
