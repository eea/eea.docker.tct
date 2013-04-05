import os
import json

def _load_json(name):
    with open(os.path.join(os.path.dirname(__file__), name), "rb") as f:
        return json.load(f)

aichi_objectives = _load_json("./be_objectives.json")
languages = ("en", "fr", "nl")

#extract actions from objectives and generate a separate file
subobj_counter = int(16)
action_counter = int(1)
action_mapper = {}
actions = []
for objective in aichi_objectives:
    # search for actions in objectives
    if len(objective["actions"]) > 1:
        print "Houston, we have a problem."
    for action in objective["actions"]:
        entry = {}
        entry["pk"] = action_counter
        entry["model"] = "nbsap.nationalaction"

        fields = {}
        for lang in languages:
            fields["title_%s" % (lang)] = action["title"][lang]

        for lang in languages:
            fields["description_%s" % (lang)] = action["body"][lang]

        entry["fields"] = fields
        action_mapper[int(objective["id"])] = action_counter
        action_counter += 1
        actions.append(entry)

    # search for actions in subobjectives
    for subobj in objective["subobjs"]:
        if len(subobj["actions"]) > 1:
            print "Houston, we have a problem."
        for action in subobj["actions"]:
            entry = {}
            entry["pk"] = action_counter
            entry["model"] = "nbsap.nationalaction"

            fields = {}
            for lang in languages:
                fields["title_%s" % (lang)] = action["title"][lang]

            for lang in languages:
                fields["description_%s" % (lang)] = action["body"][lang]

            entry["fields"] = fields
            action_mapper[subobj_counter] = action_counter
            action_counter += 1
            actions.append(entry)

        subobj_counter += 1

# extract subobjectives from objectives
import re
progo = re.compile(r"Objective\ ([0-9\.]+)\:.*")
progs = re.compile(r"Objective\ +([0-9\.]+).*")
subobj_counter = int(16)
objectives = []
for objective in aichi_objectives:
    entry = {}
    entry["pk"] = int(objective["id"])
    entry["model"] = "nbsap.nationalobjective"
    fields = {}

    try:
        code = progo.match(objective['title']['en']).groups()[0]
    except:
        import pdb; pdb.set_trace()
    fields["code"] = code
    for lang in languages:
        fields["title_%s" % (lang)] = objective["title"][lang].split(':')[1].strip()
    for lang in languages:
        fields["description_%s" % (lang)] = objective["body"][lang]
    objective_id = int(objective["id"])
    if objective_id in action_mapper:
        fields["actions"] = action_mapper[objective_id]
    entry["fields"] = fields
    objectives.append(entry)


    for subobj in objective["subobjs"]:
        if (int(objective['id']) == 4):
            continue
        entry = {}
        entry["pk"] = subobj_counter
        entry["model"] = "nbsap.nationalobjective"
        fields = {}
        try:
            code = progs.match(subobj['title']['en']).groups()[0]
        except:
            import pdb; pdb.set_trace()
        fields["code"] = code
        fields["parent"] = int(objective["id"])
        for lang in languages:
            x = subobj['title'][lang]
            if lang != 'nl':
                try:
                    fields["title_%s" % (lang)] = subobj["title"][lang].split(' ', 2)[2].strip()
                except:
                    import pdb; pdb.set_trace()
            else:
                fields["title_%s" % (lang)] = subobj["title"][lang].split(' ', 1)[1].strip()
            y = fields["title_%s" % (lang)]
        for lang in languages:
            fields["description_%s" % (lang)] = subobj["body"][lang]
        if subobj_counter in action_mapper:
            fields["actions"] = action_mapper[subobj_counter]
        entry["fields"] = fields
        subobj_counter += 1
        objectives.append(entry)

output = open("new_objectives.json", "w")
output.write(json.dumps(objectives, indent=2))
output.close()
