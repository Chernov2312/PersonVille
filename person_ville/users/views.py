__all__ = (
    'authorization',
    'character',
    'logout_view',
    'registration',
    'verify_email',
)

from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from quizzes.views import reset_quiz_progress
from users.forms import AuthorizationForm, RegisterForm
from users.models import User


def character(request):
    return render(request, 'user/character.html')


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
                current_index = request.session.get('entry_question_index', 0)

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
                'Ваш аккаунт подтверждён. ' 'Теперь вы можете войти в систему.'
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


def logout_view(request):
    reset_quiz_progress(request)
    logout(request)
    return redirect('main:main')
