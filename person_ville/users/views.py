__all__ = (
    'authorization',
    'change_email',
    'change_password',
    'history_detail',
    'history_list',
    'logout_view',
    'registration',
    'verify_email',
)

from datetime import timedelta
import random

from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import (
    urlsafe_base64_decode,
    urlsafe_base64_encode,
)

from city.managers import load_quiz_data
from quizzes.views import reset_quiz_progress
from users.forms import (
    AuthorizationForm,
    ChangeEmailConfirmForm,
    ChangeEmailRequestForm,
    ChangePasswordConfirmForm,
    ChangePasswordRequestForm,
    RegisterForm,
)
from users.models import (
    EmailChangeCode,
    PasswordChangeCode,
    User,
    UserResultHistory,
)

EMAIL_CHANGE_COOLDOWN_MINUTES = 15
PASSWORD_CHANGE_COOLDOWN_MINUTES = 10
EMAIL_CHANGE_CODE_LIFETIME_MINUTES = 10
PASSWORD_CHANGE_CODE_LIFETIME_MINUTES = 10
MAX_CHANGE_REQUEST_ATTEMPTS = 2


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.is_email_verified = False
            user.save()

            send_verification_email(request, user)

            context = {
                'title': 'Письмо отправлено',
                'message': (
                    'Мы отправили письмо на вашу почту. '
                    'Перейдите по ссылке из письма, '
                    'чтобы подтвердить аккаунт.'
                ),
            }
            return render(request, 'user/verification_sent.html', context)
    else:
        form = RegisterForm()

    context = {
        'form': form,
        'title': 'Регистрация',
    }
    return render(request, 'user/user_form.html', context)


def authorization(request):
    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        if form.is_valid():
            user = form.user

            if not user.is_email_verified or not user.is_active:
                form.add_error(
                    'login',
                    'Подтвердите email перед входом в аккаунт.',
                )
            else:
                login(request, user)

                city_result = request.session.get('city_result')
                entry_answers = request.session.get('entry_answers', {})
                current_index = request.session.get(
                    'entry_question_index',
                    0,
                )

                if city_result:
                    return redirect('city:city')

                if entry_answers or current_index > 0:
                    return redirect('quizzes:first')

                return redirect(reverse('main:main'))
    else:
        form = AuthorizationForm()

    context = {
        'form': form,
        'title': 'Авторизация',
    }
    return render(request, 'user/user_form.html', context)


def verify_email(request, uidb64, token):
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()

        context = {
            'title': 'Почта подтверждена',
            'message': (
                'Ваш аккаунт подтверждён. Теперь вы можете войти в систему.',
            ),
            'login_url': reverse('user:authorization'),
        }
        return render(request, 'user/verification_done.html', context)

    context = {
        'title': 'Ошибка подтверждения',
        'message': 'Ссылка недействительна или устарела.',
    }
    return render(request, 'user/verification_done.html', context)


def send_verification_email(request, user):
    current_site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    verify_path = reverse(
        'user:verify_email',
        kwargs={
            'uidb64': uid,
            'token': token,
        },
    )
    verify_url = request.build_absolute_uri(verify_path)

    subject = 'Подтверждение регистрации PersonVille'
    message = (
        f'Здравствуйте, {user.username}!\n\n'
        f'Подтвердите регистрацию на сайте {current_site.domain}:\n'
        f'{verify_url}\n\n'
        'Если вы не регистрировались, просто проигнорируйте это письмо.'
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )


def _build_entry_answers_for_display(snapshot, quiz_data):
    raw_answers = snapshot.get('entry_answers', {})
    answer_options = {
        item['value']: item['label']
        for item in quiz_data.get('answer_options', [])
    }

    result = []

    for index, question in enumerate(
        quiz_data.get('questions', []),
        start=1,
    ):
        raw_value = raw_answers.get(question['id'])

        if raw_value is None:
            answer_label = 'Нет ответа'
        else:
            answer_label = answer_options.get(int(raw_value), str(raw_value))

        result.append(
            {
                'number': index,
                'question': question['text'],
                'answer': answer_label,
            },
        )

    return result


def _build_house_answers_for_display(snapshot, quiz_data):
    city_result = snapshot.get('city_result', {})
    streets = city_result.get('streets', [])
    answer_options = {
        item['value']: item['label']
        for item in quiz_data.get('answer_options', [])
    }

    result = []

    for street in streets:
        houses_display = []

        for index, house in enumerate(street.get('houses', []), start=1):
            raw_value = house.get('answer_value')

            if raw_value is None:
                answer_label = 'Нет ответа'
            else:
                answer_label = answer_options.get(
                    int(raw_value),
                    str(raw_value),
                )

            houses_display.append(
                {
                    'number': index,
                    'thesis': house.get('base_text', ''),
                    'answer': answer_label,
                },
            )

        result.append(
            {
                'street_name': street.get('name', ''),
                'houses': houses_display,
            },
        )

    return result


@login_required
def history_list(request):
    history_items = UserResultHistory.objects.filter(user=request.user)

    context = {
        'history_items': history_items,
        'title': 'История прохождений',
    }
    return render(request, 'user/history_list.html', context)


@login_required
def history_detail(request, history_id):
    try:
        history_item = UserResultHistory.objects.get(
            pk=history_id,
            user=request.user,
        )
    except UserResultHistory.DoesNotExist as error:
        raise Http404('Прохождение не найдено.') from error

    quiz_data = load_quiz_data()
    snapshot = history_item.snapshot or {}
    final_character = snapshot.get('final_character', {})

    entry_answers = _build_entry_answers_for_display(snapshot, quiz_data)
    house_answers = _build_house_answers_for_display(snapshot, quiz_data)

    context = {
        'history_item': history_item,
        'character': final_character,
        'entry_answers': entry_answers,
        'house_answers': house_answers,
        'title': history_item.title,
    }
    return render(request, 'user/history_detail.html', context)


def _generate_code():
    return f'{random.randint(100000, 999999)}'


def _mask_email(email):
    if '@' not in email:
        return email

    username, domain = email.split('@', 1)

    if len(username) <= 2:
        masked_username = username[0] + '*' * max(1, len(username) - 1)
    else:
        masked_username = username[:2] + '*' * (len(username) - 2)

    return f'{masked_username}@{domain}'


def _seconds_left(value):
    if not value:
        return 0

    delta = int((value - timezone.now()).total_seconds())
    return max(0, delta)


def _iso_datetime(value):
    if not value:
        return ''

    return value.isoformat()


def _get_active_email_request(user):
    request_obj = (
        EmailChangeCode.objects.filter(
            user=user,
            is_used=False,
        )
        .order_by('-created_at')
        .first()
    )

    if request_obj and not request_obj.is_expired():
        return request_obj

    return None


def _get_active_password_request(user):
    request_obj = (
        PasswordChangeCode.objects.filter(
            user=user,
            is_used=False,
        )
        .order_by('-created_at')
        .first()
    )

    if request_obj and not request_obj.is_expired():
        return request_obj

    return None


def _count_recent_email_requests(user):
    cutoff = timezone.now() - timedelta(
        minutes=EMAIL_CHANGE_COOLDOWN_MINUTES,
    )
    return EmailChangeCode.objects.filter(
        user=user,
        created_at__gte=cutoff,
    ).count()


def _count_recent_password_requests(user):
    cutoff = timezone.now() - timedelta(
        minutes=PASSWORD_CHANGE_COOLDOWN_MINUTES,
    )
    return PasswordChangeCode.objects.filter(
        user=user,
        created_at__gte=cutoff,
    ).count()


def _set_email_change_cooldown(user):
    user.email_change_cooldown_until = timezone.now() + timedelta(
        minutes=EMAIL_CHANGE_COOLDOWN_MINUTES,
    )
    user.save(update_fields=['email_change_cooldown_until'])


def _set_password_change_cooldown(user):
    user.password_change_cooldown_until = timezone.now() + timedelta(
        minutes=PASSWORD_CHANGE_COOLDOWN_MINUTES,
    )
    user.save(update_fields=['password_change_cooldown_until'])


def _build_email_context(
    request,
    request_form,
    code_form,
    active_request,
):
    cooldown_until = request.user.email_change_cooldown_until
    cooldown_seconds = _seconds_left(cooldown_until)

    if active_request:
        title = 'Подтверждение'
        subtitle = 'Введите код из письма, чтобы завершить изменение email.'
    else:
        title = 'Новый email'
        subtitle = (
            'Укажите новый адрес. Код подтверждения мы отправим '
            'на вашу текущую почту.'
        )

    return {
        'title': title,
        'subtitle': subtitle,
        'request_form': request_form,
        'code_form': code_form,
        'active_request': active_request,
        'current_email_masked': _mask_email(request.user.email),
        'is_cooldown_active': cooldown_seconds > 0,
        'cooldown_seconds': cooldown_seconds,
        'cooldown_until_iso': _iso_datetime(cooldown_until),
    }


def _build_password_context(
    request,
    request_form,
    code_form,
    active_request,
):
    cooldown_until = request.user.password_change_cooldown_until
    cooldown_seconds = _seconds_left(cooldown_until)

    if active_request:
        title = 'Подтверждение'
        subtitle = 'Введите код из письма, чтобы завершить изменение пароля.'
    else:
        title = 'Новый пароль'
        subtitle = (
            'Укажите текущий и новый пароль. '
            'Код подтверждения мы отправим на вашу текущую почту.'
        )

    return {
        'title': title,
        'subtitle': subtitle,
        'request_form': request_form,
        'code_form': code_form,
        'active_request': active_request,
        'current_email_masked': _mask_email(request.user.email),
        'is_cooldown_active': cooldown_seconds > 0,
        'cooldown_seconds': cooldown_seconds,
        'cooldown_until_iso': _iso_datetime(cooldown_until),
    }


@login_required
def change_email(request):
    active_request = _get_active_email_request(request.user)
    request_form = ChangeEmailRequestForm(user=request.user)
    code_form = ChangeEmailConfirmForm()

    if request.method == 'POST':
        action = request.POST.get('action')
        cooldown_seconds = _seconds_left(
            request.user.email_change_cooldown_until,
        )

        if action == 'send_code':
            if cooldown_seconds > 0 or active_request:
                context = _build_email_context(
                    request,
                    request_form,
                    code_form,
                    active_request,
                )
                return render(request, 'user/change_email.html', context)

            recent_attempts = _count_recent_email_requests(request.user)
            if recent_attempts >= MAX_CHANGE_REQUEST_ATTEMPTS:
                _set_email_change_cooldown(request.user)
                context = _build_email_context(
                    request,
                    request_form,
                    code_form,
                    active_request=None,
                )
                return render(request, 'user/change_email.html', context)

            request_form = ChangeEmailRequestForm(
                request.POST,
                user=request.user,
            )

            if request_form.is_valid():
                code = _generate_code()
                new_email = request_form.cleaned_data['new_email']

                active_request = EmailChangeCode.objects.create(
                    user=request.user,
                    new_email=new_email,
                    code=code,
                    expires_at=timezone.now()
                    + timedelta(
                        minutes=EMAIL_CHANGE_CODE_LIFETIME_MINUTES,
                    ),
                    resend_available_at=timezone.now() + timedelta(minutes=1),
                )

                send_mail(
                    subject='Код подтверждения смены email PersonVille',
                    message=(
                        f'Здравствуйте, {request.user.username}!\n\n'
                        f'Код подтверждения смены email: {code}\n\n'
                        'Если это были не вы, проигнорируйте письмо.'
                    ),
                    from_email=None,
                    recipient_list=[request.user.email],
                    fail_silently=False,
                )

        elif action == 'edit_request':
            if not active_request:
                return redirect('user:change_email')

            previous_email = active_request.new_email
            active_request.is_used = True
            active_request.save(update_fields=['is_used'])
            active_request = None

            if (
                _count_recent_email_requests(request.user)
                >= MAX_CHANGE_REQUEST_ATTEMPTS
            ):
                _set_email_change_cooldown(request.user)
            else:
                request_form = ChangeEmailRequestForm(
                    user=request.user,
                    initial={'new_email': previous_email},
                )

        elif action == 'confirm_code':
            code_form = ChangeEmailConfirmForm(request.POST)

            if not active_request:
                return redirect('user:change_email')

            if code_form.is_valid():
                if active_request.is_expired():
                    code_form.add_error(
                        'code',
                        'Срок действия кода истёк.',
                    )
                elif code_form.cleaned_data['code'] != active_request.code:
                    code_form.add_error(
                        'code',
                        'Неверный код подтверждения.',
                    )
                else:
                    request.user.email = active_request.new_email
                    request.user.email_change_cooldown_until = (
                        timezone.now()
                        + timedelta(minutes=EMAIL_CHANGE_COOLDOWN_MINUTES)
                    )
                    request.user.save(
                        update_fields=[
                            'email',
                            'email_change_cooldown_until',
                        ],
                    )

                    EmailChangeCode.objects.filter(
                        user=request.user,
                        is_used=False,
                    ).update(is_used=True)

                    context = {
                        'title': 'Email изменён',
                        'message': 'Ваш email успешно обновлён.',
                    }
                    return render(
                        request,
                        'user/verification_done.html',
                        context,
                    )

    context = _build_email_context(
        request,
        request_form,
        code_form,
        active_request,
    )
    return render(request, 'user/change_email.html', context)


@login_required
def change_password(request):
    active_request = _get_active_password_request(request.user)
    request_form = ChangePasswordRequestForm(user=request.user)
    code_form = ChangePasswordConfirmForm()

    if request.method == 'POST':
        action = request.POST.get('action')
        cooldown_seconds = _seconds_left(
            request.user.password_change_cooldown_until,
        )

        if action == 'send_code':
            if cooldown_seconds > 0 or active_request:
                context = _build_password_context(
                    request,
                    request_form,
                    code_form,
                    active_request,
                )
                return render(request, 'user/change_password.html', context)

            recent_attempts = _count_recent_password_requests(request.user)
            if recent_attempts >= MAX_CHANGE_REQUEST_ATTEMPTS:
                _set_password_change_cooldown(request.user)
                context = _build_password_context(
                    request,
                    request_form,
                    code_form,
                    active_request=None,
                )
                return render(request, 'user/change_password.html', context)

            request_form = ChangePasswordRequestForm(
                request.POST,
                user=request.user,
            )

            if request_form.is_valid():
                code = _generate_code()
                password_hash = make_password(
                    request_form.cleaned_data['new_password1'],
                )

                active_request = PasswordChangeCode.objects.create(
                    user=request.user,
                    new_password_hash=password_hash,
                    code=code,
                    expires_at=timezone.now()
                    + timedelta(
                        minutes=PASSWORD_CHANGE_CODE_LIFETIME_MINUTES,
                    ),
                    resend_available_at=timezone.now() + timedelta(minutes=1),
                )

                send_mail(
                    subject='Код подтверждения смены пароля PersonVille',
                    message=(
                        f'Здравствуйте, {request.user.username}!\n\n'
                        f'Код подтверждения смены пароля: {code}\n\n'
                        'Если это были не вы, проигнорируйте письмо.'
                    ),
                    from_email=None,
                    recipient_list=[request.user.email],
                    fail_silently=False,
                )

        elif action == 'edit_request':
            if not active_request:
                return redirect('user:change_password')

            active_request.is_used = True
            active_request.save(update_fields=['is_used'])
            active_request = None

            if (
                _count_recent_password_requests(request.user)
                >= MAX_CHANGE_REQUEST_ATTEMPTS
            ):
                _set_password_change_cooldown(request.user)

        elif action == 'confirm_code':
            code_form = ChangePasswordConfirmForm(request.POST)

            if not active_request:
                return redirect('user:change_password')

            if code_form.is_valid():
                if active_request.is_expired():
                    code_form.add_error(
                        'code',
                        'Срок действия кода истёк.',
                    )
                elif code_form.cleaned_data['code'] != active_request.code:
                    code_form.add_error(
                        'code',
                        'Неверный код подтверждения.',
                    )
                else:
                    request.user.password = active_request.new_password_hash
                    request.user.password_change_cooldown_until = (
                        timezone.now()
                        + timedelta(minutes=PASSWORD_CHANGE_COOLDOWN_MINUTES)
                    )
                    request.user.save(
                        update_fields=[
                            'password',
                            'password_change_cooldown_until',
                        ],
                    )
                    update_session_auth_hash(request, request.user)

                    PasswordChangeCode.objects.filter(
                        user=request.user,
                        is_used=False,
                    ).update(is_used=True)

                    context = {
                        'title': 'Пароль изменён',
                        'message': 'Ваш пароль успешно обновлён.',
                    }
                    return render(
                        request,
                        'user/verification_done.html',
                        context,
                    )

    context = _build_password_context(
        request,
        request_form,
        code_form,
        active_request,
    )
    return render(request, 'user/change_password.html', context)


def logout_view(request):
    reset_quiz_progress(request)
    logout(request)
    return redirect('main:main')
