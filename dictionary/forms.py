from django import forms

from .models import Dictionary


POPULAR_LANGUAGE_CHOICES = [
    ("English", "English"),
    ("Spanish", "Spanish"),
    ("French", "French"),
    ("German", "German"),
    ("Italian", "Italian"),
    ("Portuguese", "Portuguese"),
    ("Japanese", "Japanese"),
    ("Korean", "Korean"),
    ("Chinese (Mandarin)", "Chinese (Mandarin)"),
    ("Arabic", "Arabic"),
    ("Russian", "Russian"),
    ("Hindi", "Hindi"),
    ("Turkish", "Turkish"),
    ("Dutch", "Dutch"),
    ("Swedish", "Swedish"),
    ("Polish", "Polish"),
    ("Greek", "Greek"),
    ("Hebrew", "Hebrew"),
    ("Norwegian", "Norwegian"),
    ("Danish", "Danish"),
    ("__custom__", "Other / add my own"),
]


class DictionaryCreateForm(forms.ModelForm):
    language = forms.ChoiceField(choices=POPULAR_LANGUAGE_CHOICES)
    custom_language = forms.CharField(
        max_length=50,
        required=False,
        help_text="Use this if your language is not in the dropdown.",
    )

    class Meta:
        model = Dictionary
        fields = ["name", "language"]

    def clean(self):
        cleaned_data = super().clean()
        language = cleaned_data.get("language")
        custom_language = (cleaned_data.get("custom_language") or "").strip()

        if language == "__custom__":
            if not custom_language:
                self.add_error("custom_language", "Enter a language name.")
            else:
                cleaned_data["language"] = custom_language

        return cleaned_data
