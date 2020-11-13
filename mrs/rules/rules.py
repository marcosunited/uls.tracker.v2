from business_rules import export_rule_data, run_all
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import Signal
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from mrs.utils.response import ResponseHttp as ObjectResponse
from mrs.models import Rule

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


def runRules(sender, instance):
    content_type = ContentType.objects.get(model=sender._meta.model_name)
    _rules = Rule.objects.filter(content_type_id=content_type.id)
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

    run_all(rule_list=rules,
            defined_variables=sender.RulesConf.variables(instance),
            defined_actions=sender.RulesConf.actions(instance),
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
