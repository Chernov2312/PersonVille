from django.shortcuts import render


def first(request):
    return render(request, 'quizzes/first_test_form.html')