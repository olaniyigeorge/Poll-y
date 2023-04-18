from django.contrib.auth.models import AbstractUser
import datetime

from users.models import UserProfile


from django.db import models

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=150)
    pub_date = models.DateTimeField("date-asked", default=datetime.datetime.now())
    description = models.TextField()
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="questions_asked")
    is_active = models.BooleanField(default=True)

    def toggle_status(self):
            if self.is_active:
                self.is_active = False
            else:
                self.is_active = True

    def __str__(self):
        return f"{self.question_text}"

    


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None, related_name="options")
    choice_text = models.CharField(max_length=150)
    votes = models.IntegerField(default=0)
    voters = models.ManyToManyField(UserProfile, blank=True, related_name="my_votes")

    def __str__(self) -> str:
        return f"{self.choice_text.capitalize()}"
