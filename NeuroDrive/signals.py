from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from NeuroDrive.models.directory import Directory


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Directory.objects.create(name="main", owner=instance)
