from business_rules import export_rule_data
from django.apps import apps
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
