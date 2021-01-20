from django.contrib.contenttypes.models import ContentType

from mrs.utils.model import to_dict


def model_processor(report, model_pk):
    data = {}
    try:
        model = ContentType.objects.get_for_id(report.content_type_id).model_class()
        instance = model.objects.get(id=model_pk)
        data = to_dict(instance)
    except ContentType.DoesNotExist:
        print("Unknown content type")
        return None
    except model.DoesNotExist:
        print("Unknown instance")
        return None

    return data
