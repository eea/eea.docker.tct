import json

scales = {
    u'G': 1,
    u'N': 2,
    u'S': 3,
    u'R': 4,
}

choices = {
    u'Low': 'low',
    u'Medium': 'med',
    u'High': 'hig',
}

aichi_file = open('aichi_indicators.json')
aichi_indicators = json.load(aichi_file)

results = []
for ind in aichi_indicators:
    entry = {}
    entry['pk'] = int(ind['id'])
    entry['model'] = "nbsap.aichiindicator"

    fields = {}
    fields['scales'] = []

    if ind.get('scale', ''):
        for scale in ind['scale'].split(','):
            fields['scales'].append(scales[scale.strip()])
    else:
        fields['scales'] = []

    fields['requirements'] = ind.get('requirements', '')
    fields['status'] = ind.get('status', '')
    fields['classification'] = ind.get('classification', '')
    fields['title'] = ind['name']
    fields['sensitivity'] = choices.get(ind.get('sensitivity', ''), '')
    fields['question'] = ind.get('question', '')

    links = []
    for link in ind.get('links', []):
        links.append('|'.join(link))
    fields['links'] = ''.join(links)

    fields['validity'] = choices.get(ind.get('validity', ''), '')
    fields['conventions'] = ind.get('conventions', '')
    fields['sub_indicator'] = ind.get('sub_indicator', '')
    fields['head_indicator'] = ind.get('head_indicator', '')
    fields['sources'] = choices.get(ind.get('sources', ''), '')
    fields['ease_of_communication'] = choices.get(ind.get('ease_of_communication', ''), '')
    fields['measurer'] = ind.get('measurer', '')

    entry['fields'] = fields

    results.append(entry)


output = open('indicators.json', 'w')
output.write(json.dumps(results, indent=2))
output.close()
