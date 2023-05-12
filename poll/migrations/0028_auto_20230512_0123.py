# Generated by Django 3.2.9 on 2023-05-12 00:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_userprofile_followers'),
        ('poll', '0027_auto_20230512_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='voters',
            field=models.ManyToManyField(blank=True, null=True, related_name='my_votes', to='users.UserProfile'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='action',
            field=models.CharField(choices=[('commented on', 'Comment'), ('liked', 'Like'), ('voted on', 'Vote'), ('followed', 'Follow')], max_length=12),
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 12, 1, 23, 23, 376725), verbose_name='date-asked'),
        ),
    ]