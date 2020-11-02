from django.db import models
from django.utils import timezone
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
    institute = models.CharField(max_length=255, null=True)
    currentleveltime= models.DateTimeField(default=timezone.now)
    is_banned = models.BooleanField(default = False)
    mostrecentanswer = models.TextField(null=True)
    lastanswertime = models.DateTimeField(default=timezone.now)
    checked = models.BooleanField(default=False)
    result = models.BooleanField(default=True)
    response = models.TextField(null=True, blank=True)
    answered = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username 
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
