import json
import os
import re
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from django.core.management.base import BaseCommand
from django.conf import settings


INDICATORS_URL = (
    'http://biodiversity.europa.eu/policy/'
    'eu-biodiversity-strategy-and-relevant-indicators')
INDICATOR_PATTERN = re.compile(
    '(?P<type>SEBI|CSI|AEI)? ?(?P<code>[\d\.]*):? ?(?P<title_en>.+)')
IGNORED = ['For all ecosystems', 'For Forests', 'For Freshwater']


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.pki = 0
        self.pkt = 0

        self.indicators = {}
        self.mapping = []
        self.existing_ind = {}

        urls = self.get_urls()
        for url in urls:
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text)
            tables = soup.find_all('table', class_='targetDesc')[1:]
            for table in tables:
                self.get_indicators_and_mapping(table)

        fixtures_path = os.path.join(settings.BASE_DIR, 'nbsap', 'fixtures')
        indicators_file = os.path.join(fixtures_path, 'eu_indicators.json')
        mapping_file = os.path.join(
            fixtures_path, 'eu_aichi_indicators_mapping.json')

        with open(indicators_file, 'w') as f:
            f.write(json.dumps(self.indicators.values(), indent=4))

        with open(mapping_file, 'w') as f:
            f.write(json.dumps(self.mapping, indent=4))

    def get_urls(self):
        resp = requests.get(INDICATORS_URL)
        soup = BeautifulSoup(resp.text)
        links = soup.find(text=re.compile('show indicators')).parent('a')
        return [link['href'] for link in links]

    def get_indicators_and_mapping(self, table):
        rows = table.find_all('tr')[1:]
        for row in rows:
            target, indicator = row('td')
            targets = [int(t.strip()) for t in target.text.split(',')] \
                if target.text else []
            children = indicator.find_all('a') or [indicator]
            for i in children:
                if isinstance(i, Tag) and i.text and i.text not in IGNORED:
                    self.add_indicator(i)
                    if not targets:
                        continue
                    self.add_mapping(targets)

    def add_indicator(self, i):
        fields = INDICATOR_PATTERN.match(i.text.strip()).groupdict()

        if fields['title_en'] in self.existing_ind:
            if fields['type']:
                self.indicators[self.label]['fields']['parent'].append(
                    self.existing_ind[fields['title_en']])
            return

        self.pki += 1

        fields['indicator_type'] = (fields.pop('type') or 'EU').lower()
        fields['url'] = i['href'] if i.name == 'a' else ''
        fields['parent'] = []

        if fields['indicator_type'] == 'eu':
            self.label = self.pki
        else:
            self.indicators[self.label]['fields']['parent'].append(self.pki)

        eu_indicator = {
            'pk': self.pki,
            'model': 'nbsap.euindicator',
            'fields': fields,
        }
        self.indicators[self.pki] = eu_indicator
        self.existing_ind[fields['title_en']] = self.pki

    def add_mapping(self, targets):
        self.pkt += 1
        self.mapping.append({
            'pk': self.pkt,
            'model': 'nbsap.euindicatortoaichistrategy',
            'fields': {
                'aichi_targets': targets,
                'eu_indicator': self.pki,
            },
        })
