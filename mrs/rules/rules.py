from django.db import models
from django.dispatch import Signal

from mrs.models import Rules

post_update = Signal()


class RulesQuerySet(models.query.QuerySet):
    def update(self, kwargs):
        super(RulesQuerySet, self).update(kwargs)
        post_update.send(sender=self.model)


class RulesManager(models.Manager):
    def getqueryset(self):
        return RulesQuerySet(self.model, using=self._db)


def getRules(contentTypeId):
    return Rules.objects.filter(content_type_id=contentTypeId)
