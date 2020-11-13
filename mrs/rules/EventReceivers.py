from django.db.models.signals import post_save
from django.dispatch import receiver

from business_rules import run_all

from mrs.models import Job
from mrs.rules.Actions import JobActions
from mrs.rules.Variables import JobVariables
from mrs.rules.rules import runRules


@receiver(post_save, sender=Job)
def post_save_job(sender, instance, created, **kwargs):
    print('recibio')

    # TODO: get rules from rules table


    runRules(sender, instance)






