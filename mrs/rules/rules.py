from business_rules import export_rule_data, run_all
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import Signal
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from mrs.models import Rule, ActionsHistory
from mrs.serializers import getDynamicSerializer
from mrs.utils.response import ResponseHttp as ObjectResponse

post_update = Signal()


class RulesQuerySet(models.query.QuerySet):
    def update(self, kwargs):
        super(RulesQuerySet, self).update()
        post_update.send(sender=self.model)


class RulesManager(models.Manager):
    def getqueryset(self):
        return RulesQuerySet(self.model, using=self._db)


def getRules(content_type_id):
    return Rule.objects.filter(content_type_id=content_type_id)


def runModelRules(sender, instance, watched_fields):
    content_type = ContentType.objects.get(model=sender._meta.model_name)
    try:
        history_entry = ActionsHistory.objects.filter(object_id=instance.id,
                                          content_type_id=content_type.id).latest('timestamp')
    except ActionsHistory.DoesNotExist:
        history_entry = None

    evaluate_rules = False
    if history_entry is not None:
        for field in watched_fields:
            if field in history_entry.model_state:
                if getattr(instance, field) != history_entry.model_state.get(field):
                    evaluate_rules = True
    else:
        evaluate_rules = True

    if evaluate_rules:
        _rules = Rule.objects.filter(content_type_id=content_type.id)
        if not _rules.exists():
            raise RulesNotDefinedError("Rules for model " + sender._meta.model_name + " not defined")
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

        serializer_class = getDynamicSerializer(sender)
        serializer = serializer_class(instance)
        json_instance = serializer.data
        ## use watched field to generate the hash
        watched_fields_value = ''
        for field_name in watched_fields:
            watched_fields_value += str(field_name) + "=" + str(getattr(instance, field_name)) + ";"
        _hash = hash(str(rules) + str(watched_fields_value))
        action_history_entry = ActionsHistory.objects.filter(hash=_hash, executed=True)

        if not action_history_entry.exists():
            rule_triggered = run_all(rule_list=rules,
                                     defined_variables=sender.RulesConf.variables(instance),
                                     defined_actions=sender.RulesConf.actions(instance),
                                     stop_on_first_trigger=True
                                     )
            if rule_triggered:
                action_history = ActionsHistory(rule=rules,
                                                variables=sender.RulesConf.variables.__name__,
                                                actions=sender.RulesConf.actions.__name__,
                                                content_type_id=content_type.id,
                                                object_id=instance.id,
                                                model_state=json_instance,
                                                hash=_hash,
                                                executed=True)
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


class RulesNotDefinedError(RuntimeError):
    def __init__(self, arg):
        self.args = arg
