# Generated by Django 3.2.9 on 2023-05-08 17:32

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_userprofile_followers'),
        ('poll', '0020_alter_question_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='likers',
            field=models.ManyToManyField(blank=True, related_name='liked_polls', to='users.UserProfile'),
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 8, 18, 32, 4, 129214), verbose_name='date-asked'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=500)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poll_comment', to='poll.question')),
            ],
        ),
    ]
