# Generated by Django 3.2.9 on 2023-05-10 09:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0024_alter_question_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 10, 10, 13, 30, 727940), verbose_name='date-asked'),
        ),
    ]
