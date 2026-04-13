__all__ = ['city_view', 'street_view']

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import redirect, render


def city_view(request):
    city_result = request.session.get('city_result')

    #if not city_result:
    #    return redirect('quizzes:first')
    
    template = 'city/city.html'
    context = {}
    return render(request=request, template_name=template, context=context)


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
