__all__ = (
    'city_view',
    'finalize_city_view',
    'street_view',
    'house_question_view',
    'character_view',
)

from copy import deepcopy

from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from city.managers import apply_house_answer
from city.managers import build_final_character
from city.managers import load_quiz_data
from users.models import UserResultHistory

STREET_SLOT_MAP = {
    'negative_emotionality': 'street-slot-top',
    'openness': 'street-slot-left',
    'conscientiousness': 'street-slot-right',
    'extraversion': 'street-slot-bottom-left',
    'agreeableness': 'street-slot-bottom-right',
}


def _get_city_result(request):
    return request.session.get('city_result')


def _find_street(city_result, trait):
    return next(
        (
            item
            for item in city_result.get('streets', [])
            if item['trait'] == trait
        ),
        None,
    )


def _find_house(street, house_id):
    return next(
        (
            item
            for item in street.get('houses', [])
            if item['house_id'] == house_id
        ),
        None,
    )


def _normalize_house_text(value):
    if isinstance(value, dict):
        return value.get('text', '')
    return value


def _refresh_street_progress(street):
    normalized_houses = []

    for index, house in enumerate(street.get('houses', []), start=1):
        if isinstance(house, str):
            normalized_houses.append(
                {
                    'house_id': f'{street["trait"]}_{index}',
                    'base_text': house,
                    'final_text': house,
                    'answer_value': None,
                    'completed': False,
                    'position': index,
                },
            )
        else:
            base_text = _normalize_house_text(
                house.get('base_text', house.get('final_text', '')),
            )
            final_text = _normalize_house_text(
                house.get('final_text', house.get('base_text', '')),
            )

            normalized_houses.append(
                {
                    'house_id': house.get(
                        'house_id',
                        f'{street["trait"]}_{index}',
                    ),
                    'base_text': base_text,
                    'final_text': final_text or base_text,
                    'answer_value': house.get('answer_value'),
                    'completed': house.get('completed', False),
                    'position': house.get('position', index),
                },
            )

    street['houses'] = normalized_houses
    street['answered_count'] = sum(
        1 for house in street['houses'] if house['completed']
    )
    street['completed'] = street['answered_count'] == len(street['houses'])
    return street


def _refresh_city_progress(city_result):
    for index, street in enumerate(city_result['streets']):
        city_result['streets'][index] = _refresh_street_progress(street)

    city_result['all_completed'] = all(
        street['completed'] for street in city_result['streets']
    )
    city_result.setdefault('is_finalized', False)
    return city_result


def city_view(request):
    city_result = _get_city_result(request)

    if not city_result:
        return redirect('quizzes:first')

    city_result = _refresh_city_progress(city_result)
    request.session['city_result'] = city_result
    request.session.modified = True

    final_character = request.session.get('final_character')
    street_slots = []

    for street in city_result['streets']:
        street_slots.append(
            {
                'trait': street['trait'],
                'name': street['name'],
                'description': street['description'],
                'answered_count': street['answered_count'],
                'houses_count': len(street['houses']),
                'slot_class': STREET_SLOT_MAP.get(street['trait'], ''),
            },
        )

    context = {
        'city_result': city_result,
        'street_slots': street_slots,
        'character_available': city_result['is_finalized'],
        'final_character': final_character,
    }
    return render(request, 'city/city.html', context)


def finalize_city_view(request):
    if request.method != 'POST':
        return redirect('city:city')

    city_result = _get_city_result(request)
    if not city_result:
        return redirect('quizzes:first')

    city_result = _refresh_city_progress(city_result)

    if city_result['is_finalized']:
        messages.info(
            request,
            'Город уже зафиксирован. Теперь можно только смотреть результат',
        )
        return redirect('city:city')

    if not city_result['all_completed']:
        messages.warning(
            request,
            'Сначала закройте тесты у всех домиков, '
            'а потом завершайте город',
        )
        return redirect('city:city')

    scored_traits = request.session.get('scored_traits', {})
    final_character = build_final_character(city_result, scored_traits)

    city_result['is_finalized'] = True
    request.session['city_result'] = city_result
    request.session['final_character'] = final_character
    request.session.modified = True

    if request.user.is_authenticated:
        snapshot = _build_result_snapshot(
            request=request,
            city_result=city_result,
            final_character=final_character,
            scored_traits=scored_traits,
        )

        UserResultHistory.objects.create(
            user=request.user,
            title=final_character.get('title', 'Итог PersonVille'),
            short_summary=final_character.get('city_summary', ''),
            snapshot=snapshot,
        )

    messages.success(
        request,
        'Город зафиксирован. Самоотчёт сохранён, и итоговый персонаж готов',
    )
    return redirect('city:city')


def street_view(request, trait):
    quiz_data = load_quiz_data()
    city_result = _get_city_result(request)

    if not city_result:
        return redirect('quizzes:first')

    city_result = _refresh_city_progress(city_result)
    request.session['city_result'] = city_result
    request.session.modified = True

    street = _find_street(city_result, trait)
    if street is None:
        raise Http404('Улица не найдена.')

    active_house = None
    active_house_id = request.GET.get('house')

    if active_house_id:
        active_house = _find_house(street, active_house_id)

    context = {
        'street': street,
        'city_result': city_result,
        'active_house': active_house,
        'question_text': quiz_data['house_correction_test'][
            'question_template'
        ],
        'answer_options': quiz_data['answer_options'],
    }
    return render(request, 'city/street.html', context)


def house_question_view(request, trait, house_id):
    quiz_data = load_quiz_data()
    city_result = _get_city_result(request)

    if not city_result:
        return redirect('quizzes:first')

    city_result = _refresh_city_progress(city_result)

    if city_result.get('is_finalized'):
        messages.info(
            request,
            'Город уже зафиксирован. Изменять ответы больше нельзя',
        )
        return redirect('city:street', trait=trait)

    street = _find_street(city_result, trait)
    if street is None:
        raise Http404('Улица не найдена.')

    house = _find_house(street, house_id)
    if house is None:
        raise Http404('Домик не найден.')

    answer_options = quiz_data['answer_options']

    if request.method == 'POST':
        raw_value = request.POST.get('answer')

        if raw_value and raw_value.isdigit():
            answer_value = int(raw_value)

            if 1 <= answer_value <= 5:
                for index, current_house in enumerate(street['houses']):
                    if current_house['house_id'] == house_id:
                        street['houses'][index] = apply_house_answer(
                            current_house,
                            answer_value,
                        )
                        break

                street = _refresh_street_progress(street)

                for index, current_street in enumerate(city_result['streets']):
                    if current_street['trait'] == trait:
                        city_result['streets'][index] = street
                        break

                city_result = _refresh_city_progress(city_result)
                request.session['city_result'] = city_result
                request.session.modified = True
                street_url = reverse('city:street', kwargs={'trait': trait})
                return redirect(f'{street_url}?house={house_id}')

    context = {
        'street': street,
        'house': house,
        'question_text': quiz_data['house_correction_test'][
            'question_template'
        ],
        'answer_options': answer_options,
    }
    return render(request, 'city/house_question.html', context)


def character_view(request):
    city_result = _get_city_result(request)
    final_character = request.session.get('final_character')

    if (
        not city_result
        or not final_character
        or not city_result.get('is_finalized')
    ):
        messages.info(
            request,
            'Сначала завершите город, чтобы открыть итоговую карточку.',
        )
        return redirect('city:city')

    context = {
        'character': final_character,
    }
    return render(request, 'city/character.html', context)


def _build_result_snapshot(
    request,
    city_result,
    final_character,
    scored_traits,
):
    return {
        'final_character': deepcopy(final_character),
        'city_result': deepcopy(city_result),
        'scored_traits': deepcopy(scored_traits),
        'entry_answers': deepcopy(request.session.get('entry_answers', {})),
        'entry_question_index': request.session.get(
            'entry_question_index',
            0,
        ),
    }
