# Generated by Django 4.0.3 on 2022-04-18 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hilt_annotation', '0004_alter_word_options'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='word',
            index=models.Index(fields=['text'], name='word_text_index'),
        ),
    ]
