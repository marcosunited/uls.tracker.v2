from django.contrib import admin

from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered


def register_models(*app_list):
    for app_name in app_list:
        app_models = apps.get_models(app_name)
        for model in app_models:
            try:
                admin.site.register(model)
            except AlreadyRegistered:
                pass


register_models('mrs')
