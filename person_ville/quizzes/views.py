__all__ = (
    'first',
    'reset_quiz_progress',
    'close_test',
    'restart_test',
)

from django.contrib import messages
from django.shortcuts import redirect, render

from city.managers import (
    build_city_from_scores,
    load_quiz_data,
    score_entry_answers,
)
from quizzes.forms import EntryAnswerForm


def reset_quiz_progress(request):
    request.session['entry_answers'] = {}
    request.session['entry_question_index'] = 0
    request.session['city_result'] = None
    request.session['scored_traits'] = None
    request.session.modified = True


def first(request):
    quiz_data = load_quiz_data()
    questions = quiz_data['questions']

    if request.GET.get('reset') == '1':
        reset_quiz_progress(request)
        return redirect('quizzes:first')

    city_result = request.session.get('city_result')
    if city_result:
        messages.info(
            request,
            'Тест уже пройден. '
            'Начните заново или перейдите к итоговому персонажу',
        )
        return redirect('main:main')

    entry_answers = request.session.get('entry_answers', {})
    current_index = request.session.get('entry_question_index', 0)

    if current_index >= len(questions):
        if not request.user.is_authenticated:
            messages.warning(
                request,
                'Войдите в аккаунт или зарегистрируйтесь, '
                'чтобы открыть карту города и сохранить свой результат',
            )
            return redirect('user:authorization')

        scored_traits = score_entry_answers(quiz_data, entry_answers)
        city_result = build_city_from_scores(quiz_data, scored_traits)

        request.session['city_result'] = city_result
        request.session['scored_traits'] = scored_traits
        request.session.modified = True

        return redirect('city:city')

    current_question = questions[current_index]

    if request.method == 'POST':
        form = EntryAnswerForm(request.POST)
        if form.is_valid():
            entry_answers[current_question['id']] = int(
                form.cleaned_data['answer'],
            )
            request.session['entry_answers'] = entry_answers
            request.session['entry_question_index'] = current_index + 1
            request.session.modified = True
            return redirect('quizzes:first')
    else:
        form = EntryAnswerForm()

    context = {
        'form': form,
        'test_title': quiz_data['meta']['title'],
        'test_description': quiz_data['meta']['description'],
        'question_text': current_question['text'],
        'question_number': current_index + 1,
        'total_questions': len(questions),
        'mode': 'entry',
    }
    return render(request, 'quizzes/table_form.html', context)


def close_test(request):

    reset_quiz_progress(request)
    return redirect('main:main')


def restart_test(request):
    reset_quiz_progress(request)
    return redirect('quizzes:first')
