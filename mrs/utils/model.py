from django.db.models import ManyToManyField


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                try:
                    data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
                except Exception as e:
                    data[f.name] = []
        else:
            data[f.name] = f.value_from_object(instance)
    return data
