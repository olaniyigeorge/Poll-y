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

    likers = models.ManyToManyField(UserProfile, blank=True, related_name="liked_polls")

    def toggle_status(self):
            if self.is_active:
                self.is_active = False
            else:
                self.is_active = True

    def __str__(self):
        return f"{self.question_text}"

    
class Comment(models.Model):
    comment_text = models.CharField(max_length=500)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="poll_comment")
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=None, related_name="comments_i_wrote")

    def __str__(self) -> str:
        return f"{self.comment_text}"

     

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None, related_name="options")
    choice_text = models.CharField(max_length=150)
    
    #TODO Remove the votes field 
    #votes = models.IntegerField(default=0)
    
    voters = models.ManyToManyField(UserProfile, blank=True, related_name="my_votes")

    def __str__(self) -> str:
        return f"{self.choice_text}"



class Notification(models.Model):
    ACTION_CHOICES = [
        ('comment', 'Comment'),
        ('like', 'Like'),
        ('vote', 'Vote'),
        ('follow', 'Follow')
    ]

    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications')
    action = models.CharField(max_length=15, choices=ACTION_CHOICES)
    action_receiver = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True, related_name='generated_impressions')
    from_who = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='activity')

    def __str__(self):
            return f'{self.from_who} {self.action}  {self.action_receiver} {self.owner}'
