#!/usr/bin/python3
import yaml

with open('np-ocp4.yaml', 'r') as f:
    parsed = yaml.safe_load(f)

templated = []
non_templated = []

for item in parsed['items']:
    print('Foor....')
    if 'allow-from-' not in item['metadata']['name'] or '-networks-to-' not in item['metadata']['name']:
        non_templated.append(item)
        continue
    if item['spec']['policyTypes'] != ['Ingress']:
        non_templated.append(item)
        continue
    if len(item['spec']['podSelector']) != 0:
        non_templated.append(item)
        continue
    if not 'ingress' in item['spec']:
        non_templated.append(item)
        continue
    if len(item['spec']['ingress']) != 1:
        non_templated.append(item)
        continue
    ingress = item['spec']['ingress']
    if len(ingress[0]['from']) != 1:
        non_templated.append(item)
        continue
    if 'namespaceSelector' not in ingress[0]['from'][0]:
        non_templated.append(item)
        continue
    ns = ingress[0]['from'][0]['namespaceSelector']
    if len(ns.keys()) != 1 or 'matchLabels' not in ns.keys():
        non_templated.append(item)
        continue
    if len(ns['matchLabels'].keys()) != 1 or 'name' not in ns['matchLabels'].keys():
        non_templated.append(item)
        continue

    templated.append(item)

with open('templated.yaml', 'w') as f:
    yaml.dump(templated, f)
with open('non-templated.yaml', 'w') as f:
    yaml.dump(non_templated, f)
