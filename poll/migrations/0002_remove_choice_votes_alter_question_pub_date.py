# Generated by Django 4.2.1 on 2023-05-23 11:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="choice",
            name="votes",
        ),
        migrations.AlterField(
            model_name="question",
            name="pub_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 5, 23, 12, 9, 12, 105501),
                verbose_name="date-asked",
            ),
        ),
    ]
