__all__ = ('EntryAnswerForm',)
from django import forms


class EntryAnswerForm(forms.Form):
    REQUIRED_ERROR_MESSAGE = {'required': 'Выбери один вариант ответа.'}
    ENTRY_ANSWER_CHOICES = [
        (1, 'Совсем не похоже'),
        (2, 'Скорее не похоже'),
        (3, 'И да, и нет'),
        (4, 'Скорее похоже'),
        (5, 'Очень похоже'),
    ]

    answer = forms.ChoiceField(
        choices=ENTRY_ANSWER_CHOICES,
        widget=forms.RadioSelect,
        label='',
        error_messages=REQUIRED_ERROR_MESSAGE,
    )
