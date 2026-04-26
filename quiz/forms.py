from django import forms

from dictionary.models import Dictionary


class QuizStartForm(forms.Form):
    dictionary = forms.ModelChoiceField(
        queryset=Dictionary.objects.none(),
        empty_label="Choose a dictionary",
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["dictionary"].queryset = Dictionary.objects.filter(owner=user).order_by("-id")


class QuizAnswerForm(forms.Form):
    selected_word_id = forms.ChoiceField(
        widget=forms.RadioSelect,
        label="Choose the correct definition",
    )

    def __init__(self, *args, choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["selected_word_id"].choices = choices or []
