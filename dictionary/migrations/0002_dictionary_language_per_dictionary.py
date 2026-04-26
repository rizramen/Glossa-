from django.db import migrations, models


LANGUAGE_MAP = {
    "en": "en",
    "english": "en",
    "de": "de",
    "german": "de",
    "es": "es",
    "spanish": "es",
    "fr": "fr",
    "french": "fr",
    "it": "it",
    "italian": "it",
}


def set_dictionary_language(apps, schema_editor):
    Dictionary = apps.get_model("dictionary", "Dictionary")
    Word = apps.get_model("dictionary", "Word")

    for dictionary in Dictionary.objects.all():
        language_code = None

        first_word = Word.objects.filter(dictionary=dictionary).order_by("id").first()
        if first_word and first_word.language:
            language_code = LANGUAGE_MAP.get(first_word.language.strip().lower())

        if language_code is None:
            language_code = LANGUAGE_MAP.get(dictionary.name.strip().lower(), "en")

        dictionary.language = language_code
        dictionary.save(update_fields=["language"])


class Migration(migrations.Migration):

    dependencies = [
        ("dictionary", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="dictionary",
            name="language",
            field=models.CharField(
                blank=True,
                choices=[
                    ("en", "English"),
                    ("de", "German"),
                    ("es", "Spanish"),
                    ("fr", "French"),
                    ("it", "Italian"),
                ],
                max_length=2,
                null=True,
            ),
        ),
        migrations.RunPython(set_dictionary_language, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="dictionary",
            name="language",
            field=models.CharField(
                choices=[
                    ("en", "English"),
                    ("de", "German"),
                    ("es", "Spanish"),
                    ("fr", "French"),
                    ("it", "Italian"),
                ],
                max_length=2,
            ),
        ),
        migrations.RemoveField(
            model_name="word",
            name="language",
        ),
    ]
