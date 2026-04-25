__all__ = ()
import http

from django.test import TestCase
from django.urls import reverse


class HomepageUrlsTests(TestCase):

    def test_main_url_reverse_returns_correct_path(self):
        url = reverse('main:main')
        self.assertEqual(url, '/')

    def test_main_url_status_code_200(self):
        response = self.client.get(reverse('main:main'))
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_nonexistent_url_returns_404(self):
        response = self.client.get('/nonexistent/')
        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)
