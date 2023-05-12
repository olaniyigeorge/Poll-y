from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.

class UserProfile(models.Model):
    display_name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='following')


    #voted_choices = models.ManyToManyField(Choice, related_name="voters")
    #asked_questions = models.ManyToManyField(Question, related_name="author")

    def __str__(self):
        return f"{self.user.username.capitalize()}"
    
    def display_name(self):
        return f"{self.user.username}"



@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
