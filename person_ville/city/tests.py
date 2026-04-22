__all__ = (
    'CityViewTests',
    'FinalizeCityViewTests',
    'StreetViewTests',
    'HouseQuestionViewTests',
    'CharacterViewTests',
)
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from city.managers import load_quiz_data


class CityViewTests(TestCase):
    def setUp(self):
        self.quiz_data = load_quiz_data()

        self.base_city_result = {
            'streets': [
                {
                    'trait': 'negative_emotionality',
                    'name': 'Улица Негативной Эмоциональности',
                    'description': 'Описание улицы',
                    'houses': [
                        {
                            'house_id': 'negative_emotionality_1',
                            'base_text': 'Тест 1',
                            'final_text': 'Тест 1',
                            'answer_value': None,
                            'completed': False,
                            'position': 1,
                        },
                        {
                            'house_id': 'negative_emotionality_2',
                            'base_text': 'Тест 2',
                            'final_text': 'Тест 2',
                            'answer_value': None,
                            'completed': False,
                            'position': 2,
                        },
                    ],
                },
                {
                    'trait': 'openness',
                    'name': 'Улица Открытости',
                    'description': 'Описание улицы открытости',
                    'houses': [
                        {
                            'house_id': 'openness_1',
                            'base_text': 'Тест 1',
                            'final_text': 'Тест 1',
                            'answer_value': None,
                            'completed': False,
                            'position': 1,
                        },
                    ],
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

    def test_city_view_without_session_redirects(self):
        response = self.client.get(reverse('city:city'))
        self.assertRedirects(response, reverse('quizzes:first'))

    def test_city_view_with_valid_session(self):
        _ = self._login_with_session(
            self.client,
            {'city_result': self.base_city_result},
        )

        response = self.client.get(reverse('city:city'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'city/city.html')
        self.assertIn('city_result', response.context)
        self.assertIn('street_slots', response.context)
        self.assertEqual(len(response.context['street_slots']), 2)

    def test_city_view_refreshes_progress(self):
        _ = self._login_with_session(
            self.client,
            {'city_result': self.base_city_result},
        )

        response = self.client.get(reverse('city:city'))

        city_result = response.context['city_result']
        for street in city_result['streets']:
            self.assertIn('answered_count', street)
            self.assertIn('completed', street)

        self.assertIn('city_result', self.client.session)

    def test_city_view_shows_final_character_when_available(self):
        session_data = {
            'city_result': self.base_city_result,
            'final_character': {
                'name': 'Тестовый персонаж',
                'description': 'Описание',
            },
        }
        _ = self._login_with_session(self.client, session_data)

        response = self.client.get(reverse('city:city'))

        self.assertEqual(
            response.context['final_character'],
            session_data['final_character'],
        )

    def test_city_view_street_slots_mapping(self):
        _ = self._login_with_session(
            self.client,
            {'city_result': self.base_city_result},
        )

        response = self.client.get(reverse('city:city'))

        street_slots = response.context['street_slots']
        for slot in street_slots:
            self.assertIn('slot_class', slot)
            if slot['trait'] == 'negative_emotionality':
                self.assertEqual(slot['slot_class'], 'street-slot-top')


class FinalizeCityViewTests(TestCase):
    def setUp(self):
        self.completed_city_result = {
            'streets': [
                {
                    'trait': 'negative_emotionality',
                    'name': 'Улица Негативной Эмоциональности',
                    'description': 'Описание',
                    'houses': [
                        {
                            'house_id': 'negative_emotionality_1',
                            'base_text': 'Тест',
                            'final_text': 'Тест',
                            'answer_value': 3,
                            'completed': True,
                            'position': 1,
                        },
                    ],
                    'answered_count': 1,
                    'completed': True,
                },
            ],
            'all_completed': True,
            'is_finalized': False,
        }

        self.scored_traits = {'negative_emotionality': 3, 'openness': 4}

    def _login_with_session(self, client, session_data=None):
        session = client.session
        if session_data:
            for key, value in session_data.items():
                session[key] = value
        session.save()
        return session

    def test_finalize_without_session_redirects(self):
        response = self.client.post(reverse('city:finalize'))
        self.assertRedirects(response, reverse('quizzes:first'))

    def test_finalize_when_already_finalized_shows_info(self):
        finalized_result = self.completed_city_result.copy()
        finalized_result['is_finalized'] = True

        _ = self._login_with_session(
            self.client,
            {'city_result': finalized_result},
        )

        response = self.client.post(reverse('city:finalize'), follow=True)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any('Город уже зафиксирован' in str(m.message) for m in messages),
        )


class StreetViewTests(TestCase):
    def setUp(self):
        self.base_city_result = {
            'streets': [
                {
                    'trait': 'negative_emotionality',
                    'name': 'Улица Негативной Эмоциональности',
                    'description': 'Описание улицы',
                    'houses': [
                        {
                            'house_id': 'negative_emotionality_1',
                            'base_text': 'Тест 1',
                            'final_text': 'Тест 1',
                            'answer_value': None,
                            'completed': False,
                            'position': 1,
                        },
                    ],
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

    def test_street_view_without_session_redirects(self):
        response = self.client.get(
            reverse('city:street', kwargs={'trait': 'openness'}),
        )
        self.assertRedirects(response, reverse('quizzes:first'))

    def test_street_view_with_invalid_trait_returns_404(self):
        _ = self._login_with_session(
            self.client,
            {'city_result': self.base_city_result},
        )

        response = self.client.get(
            reverse('city:street', kwargs={'trait': 'invalid_trait'}),
        )
        self.assertEqual(response.status_code, 404)

    def test_street_view_with_valid_trait(self):
        _ = self._login_with_session(
            self.client,
            {'city_result': self.base_city_result},
        )

        response = self.client.get(
            reverse('city:street', kwargs={'trait': 'negative_emotionality'}),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'city/street.html')
        self.assertIn('street', response.context)
        self.assertEqual(
            response.context['street']['trait'],
            'negative_emotionality',
        )

    def test_street_view_with_house_param(self):
        _ = self._login_with_session(
            self.client,
            {'city_result': self.base_city_result},
        )

        response = self.client.get(
            reverse('city:street', kwargs={'trait': 'negative_emotionality'}),
            {'house': 'negative_emotionality_1'},
        )

        self.assertIn('active_house', response.context)
        self.assertIsNotNone(response.context['active_house'])
        self.assertEqual(
            response.context['active_house']['house_id'],
            'negative_emotionality_1',
        )

    def test_street_view_with_nonexistent_house_param(self):
        _ = self._login_with_session(
            self.client,
            {'city_result': self.base_city_result},
        )

        response = self.client.get(
            reverse('city:street', kwargs={'trait': 'negative_emotionality'}),
            {'house': 'nonexistent_house'},
        )

        self.assertIsNone(response.context['active_house'])


class HouseQuestionViewTests(TestCase):
    def setUp(self):
        self.base_city_result = {
            'streets': [
                {
                    'trait': 'negative_emotionality',
                    'name': 'Улица Негативной Эмоциональности',
                    'description': 'Описание',
                    'houses': [
                        {
                            'house_id': 'negative_emotionality_1',
                            'base_text': 'Тестовый вопрос',
                            'final_text': 'Тестовый вопрос',
                            'answer_value': None,
                            'completed': False,
                            'position': 1,
                        },
                    ],
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

    def test_house_question_view_without_session_redirects(self):
        response = self.client.get(
            reverse(
                'city:house_question',
                kwargs={
                    'trait': 'negative_emotionality',
                    'house_id': 'negative_emotionality_1',
                },
            ),
        )
        self.assertRedirects(response, reverse('quizzes:first'))

    def test_house_question_view_with_finalized_city_shows_info(self):
        finalized_result = self.base_city_result.copy()
        finalized_result['is_finalized'] = True

        _ = self._login_with_session(
            self.client,
            {'city_result': finalized_result},
        )

        response = self.client.get(
            reverse(
                'city:house_question',
                kwargs={
                    'trait': 'negative_emotionality',
                    'house_id': 'negative_emotionality_1',
                },
            ),
        )

        self.assertRedirects(
            response,
            reverse('city:street', kwargs={'trait': 'negative_emotionality'}),
        )

    def test_house_question_view_with_invalid_trait_returns_404(self):
        _ = self._login_with_session(
            self.client,
            {'city_result': self.base_city_result},
        )

        response = self.client.get(
            reverse(
                'city:house_question',
                kwargs={
                    'trait': 'invalid_trait',
                    'house_id': 'negative_emotionality_1',
                },
            ),
        )
        self.assertEqual(response.status_code, 404)

    def test_house_question_view_with_invalid_house_returns_404(self):
        _ = self._login_with_session(
            self.client,
            {'city_result': self.base_city_result},
        )

        response = self.client.get(
            reverse(
                'city:house_question',
                kwargs={
                    'trait': 'negative_emotionality',
                    'house_id': 'invalid_house',
                },
            ),
        )
        self.assertEqual(response.status_code, 404)

    def test_house_question_get_request(self):
        _ = self._login_with_session(
            self.client,
            {'city_result': self.base_city_result},
        )

        response = self.client.get(
            reverse(
                'city:house_question',
                kwargs={
                    'trait': 'negative_emotionality',
                    'house_id': 'negative_emotionality_1',
                },
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'city/house_question.html')
        self.assertIn('house', response.context)
        self.assertIn('question_text', response.context)
        self.assertIn('answer_options', response.context)

    def test_house_question_post_invalid_answer(self):
        _ = self._login_with_session(
            self.client,
            {'city_result': self.base_city_result},
        )

        _ = self.client.post(
            reverse(
                'city:house_question',
                kwargs={
                    'trait': 'negative_emotionality',
                    'house_id': 'negative_emotionality_1',
                },
            ),
            {'answer': 'invalid'},
        )

        updated_session = self.client.session
        updated_house = updated_session['city_result']['streets'][0]['houses'][
            0
        ]
        self.assertFalse(updated_house['completed'])
        self.assertIsNone(updated_house['answer_value'])

    def test_house_question_post_answer_out_of_range(self):
        _ = self._login_with_session(
            self.client,
            {'city_result': self.base_city_result},
        )

        _ = self.client.post(
            reverse(
                'city:house_question',
                kwargs={
                    'trait': 'negative_emotionality',
                    'house_id': 'negative_emotionality_1',
                },
            ),
            {'answer': '10'},
        )

        updated_session = self.client.session
        updated_house = updated_session['city_result']['streets'][0]['houses'][
            0
        ]
        self.assertFalse(updated_house['completed'])


class CharacterViewTests(TestCase):
    def setUp(self):
        self.finalized_city_result = {
            'streets': [],
            'all_completed': True,
            'is_finalized': True,
        }

        self.final_character = {
            'name': 'Итоговый персонаж',
            'description': 'Описание персонажа',
            'traits': {
                'negative_emotionality': 3,
                'openness': 4,
            },
        }

    def _login_with_session(self, client, session_data=None):
        session = client.session
        if session_data:
            for key, value in session_data.items():
                session[key] = value
        session.save()
        return session

    def test_character_view_without_final_character_shows_message(self):
        _ = self._login_with_session(
            self.client,
            {'city_result': self.finalized_city_result},
        )

        response = self.client.get(reverse('city:character'), follow=True)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any('Сначала завершите город' in str(m.message) for m in messages),
        )

    def test_character_view_without_finalized_city_shows_message(self):
        not_finalized_result = self.finalized_city_result.copy()
        not_finalized_result['is_finalized'] = False

        _ = self._login_with_session(
            self.client,
            {
                'city_result': not_finalized_result,
                'final_character': self.final_character,
            },
        )

        response = self.client.get(reverse('city:character'), follow=True)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any('Сначала завершите город' in str(m.message) for m in messages),
        )

    def test_character_view_success(self):
        _ = self._login_with_session(
            self.client,
            {
                'city_result': self.finalized_city_result,
                'final_character': self.final_character,
            },
        )

        response = self.client.get(reverse('city:character'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'city/character.html')
        self.assertIn('character', response.context)
        self.assertEqual(response.context['character'], self.final_character)
