from django.db.models.signals import post_save
from django.dispatch import receiver

from mrs.models import Job
from mrs.rules.rules import runModelRules


@receiver(post_save, sender=Job)
def post_save_job(sender, instance, created, **kwargs):
    print('model event triggered')
    runModelRules(sender, instance, ['status'])






