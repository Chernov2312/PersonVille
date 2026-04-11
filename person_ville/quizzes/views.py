from django.shortcuts import redirect, render
from django.urls import reverse

from quizzes.forms import AnswerForm


def first(request):
    if request.POST:
        return redirect(reverse('city:city'))
    template = 'quizzes/table_form.html'
    context = {'form': AnswerForm()}
    return render(request, template_name=template, context=context)
