from django import forms

__all__ = ('AnswerForm',)


class AnswerForm(forms.Form):
    answer = forms.ChoiceField(
        choices=[
            ('answer1', 'Ответ 1'),
            ('answer2', 'Ответ 2'),
            ('answer3', 'Ответ 3'),
        ],
        widget=forms.RadioSelect,
        label='Выберите ответ',
        required=True,
    )