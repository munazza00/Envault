from django.db.models.signals import post_save
from django.dispatch import receiver

from projects.models import Project
from .models import Environment


@receiver(post_save, sender=Project)
def create_default_environments(sender, instance, created, **kwargs):

    if created:
        environments = [
            "development",
            "staging",
            "production",
        ]

        for environment in environments:
            Environment.objects.create(
                project=instance,
                name=environment,
            )