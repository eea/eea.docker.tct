import csv
import json
import cStringIO, codecs
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        filename = args[0]
        objs = {}

        with open(filename, 'r') as fin:
            data = json.load(fin)

            for obj in data:
                if obj['model'] not in objs:
                    objs[obj['model']] = {}
                objs[obj['model']][obj['pk']] = obj

            for _, obj in objs['tct.nationalstrategy'].items():
                eu_actions = obj['fields'].pop('eu_actions')
                for action in eu_actions:
                    action_obj = objs['tct.euaction'][action]['fields']
                    action_obj.setdefault('national_strategy', [])
                    action_obj['national_strategy'].append(obj['pk'])
                    
                eu_targets = obj['fields'].pop('eu_targets')
                for target in eu_targets:
                    target_obj = objs['tct.eutarget'][target]['fields']
                    target_obj.setdefault('national_strategy', [])
                    target_obj['national_strategy'].append(obj['pk'])

                relevant_target = obj['fields'].pop('relevant_target')
                obj['fields']['relevant_targets'] = [relevant_target]


        data = []
        for model, values in objs.items():
            data.extend(values.values())

        with open('fixed-' + filename, 'w') as fout:
            json.dump(data, fout, indent=1)
        self.stdout.write("Done")
