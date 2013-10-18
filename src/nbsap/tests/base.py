from django.db.models import Model
from django.db.models.loading import get_model

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


    def assertObjectInDatabase(self, model, **kwargs):
        if isinstance(model, basestring):
            Model = get_model('nbsap', model)
        else:
            Model = model

        if not Model:
            self.fail('Model {} does not exist'.format(model_name))
        try:
            Model.objects.get(**kwargs)
        except Model.DoesNotExist:
            self.fail('Object "{}" with kwargs {} does not exist'.format(
                model_name, str(kwargs)
            ))
