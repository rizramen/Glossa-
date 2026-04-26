from django.db import migrations, models


LANGUAGE_NAME_MAP = {
    "en": "English",
    "de": "German",
    "es": "Spanish",
    "fr": "French",
    "it": "Italian",
}


def expand_dictionary_languages(apps, schema_editor):
    Dictionary = apps.get_model("dictionary", "Dictionary")

    for dictionary in Dictionary.objects.all():
        normalized_language = (dictionary.language or "").strip().lower()
        dictionary.language = LANGUAGE_NAME_MAP.get(normalized_language, dictionary.language)
        dictionary.save(update_fields=["language"])


class Migration(migrations.Migration):

    dependencies = [
        ("dictionary", "0002_dictionary_language_per_dictionary"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dictionary",
            name="language",
            field=models.CharField(max_length=50),
        ),
        migrations.RunPython(expand_dictionary_languages, migrations.RunPython.noop),
    ]
