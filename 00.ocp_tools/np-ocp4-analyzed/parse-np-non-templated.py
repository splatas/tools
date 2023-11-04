#!/usr/bin/python3
import sys

import yaml

with open('non-templated.yaml', 'r') as f:
    parsed = yaml.safe_load(f)


templatable = []
non_templatable = []
same_namespace = []
deny_default = []


#- apiVersion: networking.k8s.io/v1
#  kind: NetworkPolicy
#  metadata:
#    name: allow-enquiry-to-accountops
#    namespace: accountops-dev
#  spec:
#    ingress:
#    - from:
#      - namespaceSelector:
#          matchLabels:
#            name: enquiry-dev
#    podSelector: {}
#    policyTypes:
#    - Ingress
# allow-from-same-namespace



for item in parsed:
    if item['metadata']['name'] == 'allow-from-same-namespace':
        same_namespace.append(item['metadata']['namespace'])
        continue
    if item['metadata']['name'] == 'deny-by-default':
        deny_default.append(item['metadata']['namespace'])
        continue
    if item['spec']['policyTypes'] != ['Ingress']:
        non_templatable.append(item)
        continue
    if len(item['spec']['podSelector']) != 0:
        non_templatable.append(item)
        continue
    if not 'ingress' in item['spec']:
        non_templatable.append(item)
        continue
    if len(item['spec']['ingress']) != 1:
        non_templatable.append(item)
        continue
    ingress = item['spec']['ingress']
    if len(ingress[0]['from']) != 1:
        non_templatable.append(item)
        continue
    if 'namespaceSelector' not in ingress[0]['from'][0]:
        non_templatable.append(item)
        continue
    ns = ingress[0]['from'][0]['namespaceSelector']
    if len(ns.keys()) != 1 or 'matchLabels' not in ns.keys():
        non_templatable.append(item)
        continue
    if len(ns['matchLabels'].keys()) != 1 or 'name' not in ns['matchLabels'].keys():
        non_templatable.append(item)
        continue

    to_namespace = item['metadata']['namespace']
    from_namespace = ingress[0]['from'][0]['namespaceSelector']['matchLabels']['name']

    templatable.append({
        'from': from_namespace,
        'to': to_namespace,
        'name': item['metadata']['name'],
        'item': item,
    })


with open('allow-same-namespace.yaml', 'w') as f:
    yaml.dump(same_namespace, f)
with open('deny-by-default.yaml', 'w') as f:
    yaml.dump(deny_default, f)
with open('templatable.yaml', 'w') as f:
    yaml.dump(templatable, f)
with open('non-templatable.yaml', 'w') as f:
    yaml.dump(non_templatable, f)
