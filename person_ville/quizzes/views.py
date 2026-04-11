from django.shortcuts import redirect, render
from django.urls import reverse


def first(request):
    if request.POST:
        return redirect(reverse('city:city'))
    return render(request, 'quizzes/table_form.html')
