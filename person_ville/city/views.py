__all__ = ['city_view', 'street_view']

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import redirect


def city_view(request):
    city_result = request.session.get('city_result')

    if not city_result:
        return redirect('quizzes:first')

    return HttpResponse(
        'Город собран. Фронт улиц будет подключён позже.',
    )


def street_view(request, trait):
    city_result = request.session.get('city_result')

    if not city_result:
        return redirect('quizzes:first')

    streets = city_result.get('streets', [])
    street = next(
        (
            item
            for item in streets
            if item['trait'] == trait
        ),
        None,
    )

    if street is None:
        raise Http404('Улица не найдена.')

    return HttpResponse(
        f'Улица "{street["name"]}". Фронт будет подключён позже.',
    )
