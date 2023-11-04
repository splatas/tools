#!/usr/bin/python3
import sys

import yaml

with open('templated.yaml', 'r') as f:
    parsed = yaml.safe_load(f)

#- from: enquiry-dev
#  name: allow-enquiry-to-accountops
#  to: accountops-dev

templated = []
inaccurate = []

for item in parsed:
    name = item['metadata']['name']
    name = name[len('allow-from-'):]
    to_start = name.find('-networks-to-')
    to_name = name[to_start + len('-networks-to-'):]
    name = name[:to_start]

    to_namespace = item['metadata']['namespace']
    try:
        from_namespace = item['spec']['ingress'][0]['from'][0]['namespaceSelector']['matchLabels']['name']
    except:
        inaccurate.append(item)
        continue

    if to_namespace != to_name:
        inaccurate.append(item)
    if from_namespace != name:
        inaccurate.append(item)

    templated.append({
        'from': from_namespace,
        'to': to_namespace,
        'name': item['metadata']['name'],
        'item': item,
    })


with open("templated-list.yaml", "w") as f:
    yaml.dump(templated, f)
with open("templated-inaccurate.yaml", "w") as f:
    yaml.dump(inaccurate, f)
