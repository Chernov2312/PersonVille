from django.shortcuts import redirect, render
from django.urls import reverse

from quizzes.forms import AnswerForm


def first(request, number):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid() and number == 15:
            return redirect(reverse('city:city'))
        elif form.is_valid():
            return redirect('quizzes:first', number=number + 1)
    template = 'quizzes/table_form.html'
    context = {'form': AnswerForm(), 'number': number + 1}
    return render(request, template_name=template, context=context)
