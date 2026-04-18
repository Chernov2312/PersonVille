__all__ = ('EntryAnswerForm', 'StreetCorrectionForm')
from django import forms

REQUIRED_ERROR_MESSAGE = {'required': 'Выбери один вариант ответа.'}
ENTRY_ANSWER_CHOICES = [
    (1, 'Совсем не похоже'),
    (2, 'Скорее не похоже'),
    (3, 'И да, и нет'),
    (4, 'Скорее похоже'),
    (5, 'Очень похоже'),
]


class EntryAnswerForm(forms.Form):
    answer = forms.ChoiceField(
        choices=ENTRY_ANSWER_CHOICES,
        widget=forms.RadioSelect,
        label='',
        error_messages=REQUIRED_ERROR_MESSAGE,
    )


class StreetCorrectionForm(forms.Form):
    answer = forms.ChoiceField(
        choices=[],
        widget=forms.RadioSelect,
        label='',
        error_messages=REQUIRED_ERROR_MESSAGE,
    )

    def __init__(self, *args, choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        if choices is not None:
            self.fields['answer'].choices = choices
