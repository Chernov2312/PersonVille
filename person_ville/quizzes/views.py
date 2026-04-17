__all__ = [
    'first',
    'street_correction',
    'reset_quiz_progress',
    'close_test',
    'restart_test',
]

from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from city.managers import apply_street_correction
from city.managers import build_city_from_scores
from city.managers import load_quiz_data
from city.managers import score_entry_answers
from quizzes.forms import EntryAnswerForm
from quizzes.forms import StreetCorrectionForm


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


def street_correction(request, trait):
    quiz_data = load_quiz_data()
    city_result = request.session.get('city_result')

    if not city_result:
        return redirect('quizzes:first')

    streets = city_result.get('streets', [])
    street_index = next(
        (
            index
            for index, item in enumerate(streets)
            if item['trait'] == trait
        ),
        None,
    )

    if street_index is None:
        raise Http404('Улица не найдена.')

    street = streets[street_index]
    correction_test = quiz_data['street_correction_test']
    correction_choices = [
        (option['code'], option['label'])
        for option in correction_test['options']
    ]

    if request.method == 'POST':
        form = StreetCorrectionForm(
            request.POST,
            choices=correction_choices,
        )
        if form.is_valid():
            answer_code = form.cleaned_data['answer']
            updated_street = apply_street_correction(
                street,
                quiz_data,
                answer_code,
            )

            streets[street_index] = updated_street
            city_result['streets'] = streets
            request.session['city_result'] = city_result
            request.session.modified = True

            return redirect('city:street', trait=trait)
    else:
        form = StreetCorrectionForm(
            choices=correction_choices,
        )

    context = {
        'form': form,
        'street': street,
        'test_title': correction_test['title'],
        'test_description': correction_test['description'],
        'question_text': correction_test['question'],
        'question_number': 1,
        'total_questions': 1,
        'mode': 'street',
    }
    return render(request, 'quizzes/table_form.html', context)


def close_test(request):
    reset_quiz_progress(request)
    return redirect('main:main')


def restart_test(request):
    reset_quiz_progress(request)
    return redirect('quizzes:first')
