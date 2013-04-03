import os
import json

def _load_json(name):
    with open(os.path.join(os.path.dirname(__file__), name), "rb") as f:
        return json.load(f)

aichi_goals = _load_json("./aichi_goals.json")
aichi_targets = _load_json("./aichi_targets.json")

results = []

languages = ('en', 'fr', 'nl')

for goal in aichi_goals:
    entry = {}
    entry['pk'] = int(goal['id'])
    entry['model'] = "nbsap.aichigoal"

    fields = {}
    fields["targets"] = []

    for lang in languages:
        fields["title_%s" % (lang)] = goal["title"][lang]

    for lang in languages:
        fields["description_%s" % (lang)] = goal["description"][lang]

    current_literal_id = goal['short_title']
    for target in aichi_targets:
        if 'goal_id' in target:
            if target['goal_id'] == current_literal_id:
                fields['targets'].append(int(target['id']))

    entry['fields'] = fields
    results.append(entry)


output = open('new_goals.json', 'w')
output.write(json.dumps(results, indent=2))
output.close()


