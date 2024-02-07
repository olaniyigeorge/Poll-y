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

    def __str__(self):
            return f"{self.question_text}"

    def toggle_status(self):
            if self.is_active:
                self.is_active = False
            else:
                self.is_active = True

    def get_likes_count(self) -> int:
        return self.likers.count()

    def get_options(self) -> list:
        return self.options.all() 

    
    
class Comment(models.Model):
    comment_text = models.CharField(max_length=500)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="poll_comment")
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=None, related_name="comments_i_wrote")

    def __str__(self) -> str:
        return f"{self.comment_text}"
    

    def generate_notification(self):
        n = Notification()
        
         


     

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None, related_name="options")
    choice_text = models.CharField(max_length=150)
    voters = models.ManyToManyField(UserProfile, blank=True, related_name="my_votes")


    def __str__(self) -> str:
        return f"{self.choice_text}"

    def get_voters_count(self):
        return self.voters.count()
    
    def get_voters_(self):
        return list(self.voters.all())
    

        


class Notification(models.Model):
    ACTION_CHOICES = [
        ('comment', 'Comment'),
        ('like', 'Like'),
        ('vote', 'Vote'),
        ('follow', 'Follow'),
        ('unfollow', 'Unfollow')
    ]

    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications')
    action = models.CharField(max_length=15, choices=ACTION_CHOICES)
    action_receiver = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True, related_name='generated_impressions')
    from_who = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='activity')

    def __str__(self):
            return f'{self.from_who} {self.action}  {self.action_receiver} {self.owner}'
