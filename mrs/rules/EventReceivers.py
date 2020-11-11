from django.db.models.signals import post_save
from django.dispatch import receiver

from business_rules import run_all

from mrs.models import Job
from mrs.rules.Actions import JobActions
from mrs.rules.Variables import JobVariables


@receiver(post_save, sender=Job)
# TODO: extend @receiver get the sender contenttype,
# check the table rules and pass all rules for the content type as rules parameter
def post_save_job(sender, instance, created, **kwargs):
    print('recibio')

    rules = [
        # expiration_days < 5 AND current_inventory > 20
        {"conditions": {"all": [
            {"name": "lifts_count",
             "operator": "less_than",
             "value": 5,
             },
        ]},
            "actions": [
                {"name": "update_contract",
                 "params": {"contract_addition": 'addition type'},
                },
            ],
        },
    ]

    run_all(rule_list=rules,
            defined_variables=JobVariables(instance),
            defined_actions=JobActions(instance),
            stop_on_first_trigger=True
            )






