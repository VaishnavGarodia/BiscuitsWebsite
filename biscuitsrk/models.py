from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class QuestionsModel(models.Model):
    level = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentlevel = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username

class Resp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # def __str__(self):
    #     return self.user.username+" "+self
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
