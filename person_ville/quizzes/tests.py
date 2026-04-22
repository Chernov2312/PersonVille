__all__ = (
    'QuizzesFirstViewTests',
    'QuizzesStreetCorrectionTests',
    'QuizzesCloseTestTests',
    'QuizzesRestartTestTests',
)

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from city.managers import load_quiz_data


class QuizzesFirstViewTests(TestCase):
    def setUp(self):
        self.quiz_data = load_quiz_data()
        self.questions_count = len(self.quiz_data['questions'])

    def _login_with_session(self, client, session_data=None):
        session = client.session
        if session_data:
            for key, value in session_data.items():
                session[key] = value
        session.save()
        return session

    def test_first_view_without_session_shows_first_question(self):
        response = self.client.get(reverse('quizzes:first'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quizzes/table_form.html')
        self.assertIn('form', response.context)
        self.assertIn('question_text', response.context)
        self.assertEqual(response.context['question_number'], 1)
        self.assertEqual(
            response.context['total_questions'],
            self.questions_count,
        )

    def test_first_view_with_reset_param_clears_session(self):
        session = self.client.session
        session['entry_answers'] = {1: 3}
        session['entry_question_index'] = 5
        session['city_result'] = {'test': 'data'}
        session.save()

        _ = self.client.post(reverse('quizzes:first'), {'reset': '1'})

        session = self.client.session
        self.assertEqual(session.get('entry_answers'), {})
        self.assertEqual(session.get('entry_question_index'), 0)
        self.assertIsNone(session.get('city_result'))

    def test_first_view_with_city_result_shows_message(self):
        _ = self._login_with_session(
            self.client,
            {'city_result': {'streets': [], 'all_completed': False}},
        )

        response = self.client.get(reverse('quizzes:first'), follow=True)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any('Тест уже пройден' in str(m.message) for m in messages),
        )
        self.assertRedirects(response, reverse('main:main'))

    def test_first_view_post_valid_answer(self):
        response = self.client.post(
            reverse('quizzes:first'),
            {'answer': '3'},
        )

        self.assertRedirects(response, reverse('quizzes:first'))
        self.assertIn('entry_answers', self.client.session)
        self.assertEqual(
            self.client.session['entry_question_index'],
            1,
        )

    def test_first_view_post_invalid_answer(self):
        response = self.client.post(
            reverse('quizzes:first'),
            {'answer': 'invalid'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quizzes/table_form.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_first_view_completes_all_questions_redirects_to_auth_for_anon(
        self,
    ):
        questions = self.quiz_data['questions']
        session = self.client.session
        entry_answers = {str(q['id']): 3 for q in questions}
        session['entry_answers'] = entry_answers
        session['entry_question_index'] = len(questions)
        session.save()

        response = self.client.get(reverse('quizzes:first'))

        self.assertRedirects(response, reverse('user:authorization'))
        self.assertNotIn('city_result', self.client.session)


class QuizzesStreetCorrectionTests(TestCase):
    def setUp(self):
        self.quiz_data = load_quiz_data()
        self.base_city_result = {
            'streets': [
                {
                    'trait': 'negative_emotionality',
                    'name': 'Улица Негативной Эмоциональности',
                    'description': 'Описание',
                    'houses': [
                        {
                            'house_id': 'negative_emotionality_1',
                            'answer_value': 3,
                            'completed': True,
                        },
                    ],
                    'answered_count': 1,
                    'completed': False,
                },
                {
                    'trait': 'openness',
                    'name': 'Улица Открытости',
                    'description': 'Описание',
                    'houses': [],
                    'answered_count': 0,
                    'completed': False,
                },
            ],
            'all_completed': False,
            'is_finalized': False,
        }

    def _login_with_session(self, client, session_data=None):
        session = client.session
        if session_data:
            for key, value in session_data.items():
                session[key] = value
        session.save()
        return session


class QuizzesCloseTestTests(TestCase):
    def test_close_test_clears_session_and_redirects_to_main(self):
        session = self.client.session
        session['entry_answers'] = {1: 3}
        session['city_result'] = {'test': 'data'}
        session.save()

        response = self.client.post(reverse('quizzes:close'))

        self.assertRedirects(response, reverse('main:main'))
        session = self.client.session
        self.assertEqual(session.get('entry_answers'), {})
        self.assertIsNone(session.get('city_result'))

    def test_close_test_with_empty_session(self):
        response = self.client.post(reverse('quizzes:close'))
        self.assertRedirects(response, reverse('main:main'))


class QuizzesRestartTestTests(TestCase):
    def test_restart_test_clears_session_and_redirects_to_first(self):
        session = self.client.session
        session['entry_answers'] = {1: 3, 2: 5}
        session['entry_question_index'] = 3
        session['city_result'] = {'streets': []}
        session['scored_traits'] = {'extraversion': 4}
        session.save()

        response = self.client.post(reverse('quizzes:restart'))

        self.assertRedirects(response, reverse('quizzes:first'))
        session = self.client.session
        self.assertEqual(session.get('entry_answers'), {})
        self.assertIsNone(session.get('city_result'))
        self.assertIsNone(session.get('scored_traits'))

    def test_restart_test_with_empty_session(self):
        response = self.client.post(reverse('quizzes:restart'))
        self.assertRedirects(response, reverse('quizzes:first'))


class QuizzesUrlTests(TestCase):
    def test_first_url_reverse(self):
        url = reverse('quizzes:first')
        self.assertEqual(url, '/quiz/')

    def test_close_url_reverse(self):
        url = reverse('quizzes:close')
        self.assertEqual(url, '/quiz/close/')

    def test_restart_url_reverse(self):
        url = reverse('quizzes:restart')
        self.assertEqual(url, '/quiz/restart/')
