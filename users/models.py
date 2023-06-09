from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.

class UserProfile(models.Model):
    display_name = models.CharField(max_length=100, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='following')


    def __str__(self):
        return f"{self.user.username}"
    
    """ def display_name(self, name):
        if name:
            self.display_name = name
        else:
            if self.display_name == "":
                self.display_name = self.user.username
        
        return f"{self.display_name}"  """
   
    
    


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
