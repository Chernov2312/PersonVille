__all__ = ()
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from users.models import User, UserResultHistory


class UserModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='player',
            is_email_verified=True,
        )
        cls.user_with_cooldown = User.objects.create_user(
            username='cooldownuser',
            email='cooldown@example.com',
            password='testpass123',
            role='player',
            email_change_cooldown_until=timezone.now() + timedelta(days=1),
            password_change_cooldown_until=timezone.now()
            + timedelta(hours=12),
        )

    def test_user_creation_with_defaults(self):
        user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='newpass123',
        )
        self.assertEqual(user.role, 'player')
        self.assertFalse(user.is_email_verified)
        self.assertIsNone(user.email_change_cooldown_until)
        self.assertIsNone(user.password_change_cooldown_until)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)

    def test_role_validation(self):
        user = User.objects.create_user(
            username='validrole',
            email='valid@example.com',
            password='testpass123',
            role='admin',
        )
        self.assertEqual(user.role, 'admin')

        user_invalid = User(
            username='invalidrole',
            email='invalid@example.com',
            password='testpass123',
            role='invalid_role_name',
        )
        with self.assertRaises(ValidationError):
            user_invalid.full_clean()

    def test_email_change_cooldown_field(self):
        self.assertIsNotNone(
            self.user_with_cooldown.email_change_cooldown_until,
        )
        self.assertGreater(
            self.user_with_cooldown.email_change_cooldown_until,
            timezone.now(),
        )


class UserResultHistoryModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='historyuser',
            email='history@example.com',
            password='testpass123',
        )

        now = timezone.now()
        one_day_ago = now - timedelta(days=1)
        two_days_ago = now - timedelta(days=2)

        cls.history_1 = UserResultHistory.objects.create(
            user=cls.user,
            title='Test Result 1',
            short_summary='Completed successfully',
            snapshot={'score': 100, 'level': 5},
        )
        UserResultHistory.objects.filter(pk=cls.history_1.pk).update(
            created_at=one_day_ago,
        )

        cls.history_2 = UserResultHistory.objects.create(
            user=cls.user,
            title='Test Result 2',
            short_summary='Failed at level 3',
            snapshot={'score': 45, 'level': 3, 'reason': 'timeout'},
        )
        UserResultHistory.objects.filter(pk=cls.history_2.pk).update(
            created_at=two_days_ago,
        )

    def test_result_history_creation(self):
        history = UserResultHistory.objects.create(
            user=self.user,
            title='New Test',
            short_summary='Test summary',
            snapshot={'key': 'value', 'nested': {'data': 123}},
        )
        self.assertEqual(history.user, self.user)
        self.assertEqual(history.title, 'New Test')
        self.assertEqual(history.short_summary, 'Test summary')
        self.assertDictEqual(
            history.snapshot,
            {'key': 'value', 'nested': {'data': 123}},
        )
        self.assertIsNotNone(history.created_at)

    def test_result_history_ordering(self):
        histories = UserResultHistory.objects.all()
        self.assertEqual(histories.count(), 2)
        self.assertEqual(histories[0], self.history_1)
        self.assertEqual(histories[1], self.history_2)
        self.assertGreater(histories[0].created_at, histories[1].created_at)

    def test_result_history_str_method(self):
        expected_str = f'{self.user.username}: {self.history_1.title}'
        self.assertEqual(str(self.history_1), expected_str)

    def test_result_history_verbose_names(self):
        meta = UserResultHistory._meta
        self.assertEqual(meta.get_field('user').verbose_name, 'Пользователь')
        self.assertEqual(
            meta.get_field('title').verbose_name,
            'Название результата',
        )
        self.assertEqual(meta.verbose_name, 'История прохождения')
        self.assertEqual(meta.verbose_name_plural, 'История прохождений')
