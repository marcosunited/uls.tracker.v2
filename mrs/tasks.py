from background_task import background
from business_rules import run_all
from django.apps import apps

from mrs.models import ProgrammedTask
from mrs.utils.filter import DynamicFilter


#@background(schedule=5)
def master_programmed_task():
    print('llego aca')
    dynamic_filter = DynamicFilter()
    programmed_tasks = ProgrammedTask.objects.filter(active=True)
    for task in programmed_tasks:
        model = apps.get_model('mrs', task.content_type.model)
        query_set = dynamic_filter.filter(model.objects.all(), task.filter)
        for instance in query_set:
            runRules(task.conditions['rules'],
                     model.RulesConf.variables(instance),
                     model.RulesConf.actions(instance))


def runRules(rules, variables, actions):
    run_all(rule_list=rules,
            defined_variables=variables,
            defined_actions=actions,
            stop_on_first_trigger=True)
