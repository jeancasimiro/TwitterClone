from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class Tweet(models.Model):
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.content[:50]
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()    