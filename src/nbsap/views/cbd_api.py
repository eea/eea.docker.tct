import json
import requests

from django.conf import settings
from django.http import JsonResponse
from django.utils import translation

from nbsap import models


MODEL_TO_SCHEMA = {
    models.NationalObjective: 'nationalTarget',
}


def get_token():
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;Charset=utf-8',
    }
    credentials = {
        'email': settings.CBD_API_USERNAME,
        'password': settings.CBD_API_PASSWORD,
    }
    payload = json.dumps(credentials)
    resp = requests.post(settings.CBD_AUTH_URL, payload, headers=headers,
                         verify=settings.CBD_VERIFY_SSL)
    if resp.status_code not in (200, 201):
        return
    return resp.json().get('authenticationToken')


def get_cbd_obj(model_cls, pk, schema):
    obj = model_cls.objects.get(pk=pk)
    cbd_id = 'TCT-{}-{}'.format(model_cls.__name__, pk)
    languages = [code for code, name in settings.LANGUAGES
                 if code in settings.CBD_API_LANGUAGES]

    cbd_obj = {
        'header': {
            'identifier': cbd_id,
            'languages': languages,
            'schema': schema,
        },
        'government': {'identifier': 'eu'},
        'title': {},
        'description': {},
    }

    for lang in languages:
        translation.activate(lang)
        cbd_obj['title'][lang] = obj.title
        cbd_obj['description'][lang] = obj.description

    return cbd_obj


def create_workflow(new_document, headers):
    workflow_data = {
        'type': 'publishNationalRecord',
        'version': '0.4',
        'data': {
            'realm': new_document['realm'],
            'documentID': new_document['workingDocumentID'],
            'identifier': new_document['identifier'],
            'title': new_document['workingDocumentTitle'],
            'abstract': new_document['workingDocumentSummary'],
            'metadata': new_document['workingDocumentMetadata'],
        }
    }
    payload = json.dumps(workflow_data)
    resp = requests.post(settings.CBD_WORKFLOW_URL, payload, headers=headers,
                         verify=settings.CBD_VERIFY_SSL)
    return resp.status_code in (200, 201)


def send_to_cbd(request, model_name, pk):
    if request.method == 'POST':
        token = get_token()
        if not token:
            return JsonResponse({
                'status': 'error',
                'message': 'Could not get authentication token.',
            })

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;Charset=utf-8',
            'Realm': settings.CBD_API_REALM,
            'Authorization': 'Ticket {}'.format(token),
        }

        model_cls = getattr(models, model_name)
        schema = MODEL_TO_SCHEMA.get(model_cls)

        cbd_obj = get_cbd_obj(model_cls, pk, schema)
        uid = cbd_obj['header']['identifier']
        url = settings.CBD_SAVE_URL.format(uid=uid, schema=schema)

        payload = json.dumps(cbd_obj)

        resp = requests.put(url, payload, headers=headers,
                            verify=settings.CBD_VERIFY_SSL)
        if resp.status_code in (200, 201):
            status = 'success'
            message = 'Successfully sent object to CBD.'

            new_document = resp.json()
            if not create_workflow(new_document, headers):
                message += ' Failed to create workflow.'
        else:
            error_message = resp.json().get('Message')
            status = 'error'
            message = 'Could not send object to CBD. {}'.format(error_message)
        return JsonResponse({
            'status': status,
            'message': message,
        })
