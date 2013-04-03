import os
import json

def _load_json(name):
    with open(os.path.join(os.path.dirname(__file__), name), "rb") as f:
        return json.load(f)

aichi_indicators = _load_json("./aichi_indicators.json")
aichi_targets = _load_json("./aichi_targets.json")

results = []

languages = ('en', 'fr', 'nl')

for target in aichi_targets:
    entry = {}
    entry['pk'] = int(target['id'])
    entry['model'] = "nbsap.aichitarget"

    fields = {}
    fields["other_indicators"] = []
    fields["indicators"] = []

    for lang in languages:
        fields["title_%s" % (lang)] = target["title"][lang]

    for lang in languages:
        fields["description_%s" % (lang)] = target["description"][lang]


    current_id = int(target['id'])
    for indicator in aichi_indicators:
        if 'relevant_target' in indicator:
            if current_id == int(indicator["relevant_target"]):
                fields['indicators'].append(int(indicator['id']))

        if 'other_targets' in indicator:
            for ind_other_target in indicator["other_targets"]:
                if not ind_other_target:
                    continue
                try:
                    if current_id == int(ind_other_target):
                        fields['other_indicators'].append(int(indicator['id']))
                except Exception:
                    pass

    entry['fields'] = fields
    results.append(entry)


output = open('new_targets.json', 'w')
output.write(json.dumps(results, indent=2))
output.close()
