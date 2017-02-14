from django.db.models import Model
from django.apps import apps
from django.conf import settings

from django_webtest import WebTest
from webtest.forms import Select, MultipleSelect


class BaseWebTest(WebTest):

    def populate_fields(self, form, data):
        for field_name, field in form.field_order:
            if field_name in data:
                value = data[field_name]
                if isinstance(value, Model):
                    value = value.pk
                if isinstance(field, MultipleSelect):
                    if not isinstance(value, list):
                        value = [value]
                if isinstance(field, (Select, MultipleSelect)):
                    field.force_value(value)
                else:
                    field.value = value
        return form

    def normalize_data(self, data):
        for k, v in data.items():
            if isinstance(v, Model):
                data[k] = v.pk
        return data

    def assertObjectInDatabase(self, model, kwargs):
        if isinstance(model, basestring):
            Model = apps.get_model('nbsap', model)
        else:
            Model = model

        kwargs_copy = {}
        for k, v in kwargs.items():
            if '_default' in k:
                k = k.replace('_default', '_' + settings.LANGUAGE_CODE)
            kwargs_copy[k] = v
        kwargs = kwargs_copy

        if not Model:
            self.fail('Model {} does not exist'.format(model))
        try:
            return Model.objects.get(**kwargs)
        except Model.DoesNotExist:
            self.fail('Object "{}" with kwargs {} does not exist'.format(
                model, str(kwargs)
            ))
