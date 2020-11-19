from auditlog.models import LogEntry
from business_rules import export_rule_data, run_all
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import Signal
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from mrs.serializers import getDynamicSerializer
from mrs.utils.response import ResponseHttp as ObjectResponse
from mrs.models import Rule, ActionsHistory

post_update = Signal()


class RulesQuerySet(models.query.QuerySet):
    def update(self, kwargs):
        super(RulesQuerySet, self).update(kwargs)
        post_update.send(sender=self.model)


class RulesManager(models.Manager):
    def getqueryset(self):
        return RulesQuerySet(self.model, using=self._db)


def getRules(content_type_id):
    return Rule.objects.filter(content_type_id=content_type_id)


def runModelRules(sender, instance, watched_fields):
    content_type = ContentType.objects.get(model=sender._meta.model_name)
    log_entry = LogEntry.objects.filter(object_pk=instance.id,
                                        content_type_id=content_type.id).latest('timestamp')
    evaluate_rules = False
    for field in watched_fields:
        if field in log_entry.changes_dict:
            evaluate_rules = True

    if evaluate_rules:
        _rules = Rule.objects.filter(content_type_id=content_type.id)
        if not _rules.exists():
            raise RulesNotDefiniedError("Rules for model " + sender._meta.model_name + " not defined")
        # TODO: add entry to rule history, storage result of evaluation and result of associate action
        rules = []
        rules_count = 0
        for rule in _rules:
            try:
                rules.append(rule.conditions['rules'][rules_count])
                rules_count = rules_count + 1
            except KeyError as e:
                print(str(e))
            except IndexError as e:
                print(str(e))

        rule_triggered = run_all(rule_list=rules,
                                 defined_variables=sender.RulesConf.variables(instance),
                                 defined_actions=sender.RulesConf.actions(instance),
                                 stop_on_first_trigger=True
                                 )
        if rule_triggered:
            serializer_class = getDynamicSerializer(sender)
            serializer = serializer_class(instance)
            json_instance = serializer.data
            action_history = ActionsHistory(rule=rules,
                                            content_type_id=content_type.id,
                                            object_id=instance.id,
                                            model_state=json_instance)
            action_history.save()

def runRules(rule_id, variables, actions, data):
    rule = Rule.objects.get(pk=rule_id)
    run_all(rule_list=rule.conditions['rules'],
            defined_variables=variables(data),
            defined_actions=actions(data),
            stop_on_first_trigger=True
            )


class RulesMetaView(APIView):

    def get(self, request, model):
        _model = apps.get_model('mrs', model)

        try:
            meta = export_rule_data(_model.RulesConf.variables,
                                    _model.RulesConf.actions)
            response = ObjectResponse(meta)
        except AttributeError as e:
            response = ObjectResponse(error='Rules not configured for model ' + model)
        return Response(response.result, status=HTTP_200_OK)


class RulesNotDefiniedError(RuntimeError):
    def __init__(self, arg):
        self.args = arg
