#!/usr/bin/python3
import sys

import yaml

envs = ['dev', 'pre-sit', 'sit', 'uat']
# These were found in the network policies, but were not actually in the Ansible playbooks
envs.extend([
    'mr',
    'sit1',
    'sit2',
    'sit3',
    'sit-v2',
    'test',
    'uat1',
    'rnd',
])

def get_name_env(item, is_from):
    if is_from:
        name = item['from']
        namespace = item['item']['spec']['ingress'][0]['from'][0]['namespaceSelector']['matchLabels']['name']
    else:
        name = item['to']
        namespace = item['item']['metadata']['namespace']

    if name == 'default' or namespace == 'default' or name == 'kube-system' or namespace == 'kube-system':
        return (name, 'ClusterWide')
    for env in envs:
        if name.endswith(f'-{env}'):
            name = name[:-len(env)-1]
            return (name, env)
        if namespace.endswith(f'-{env}'):
            namespace = namespace[:-len(env)-1]
            return (namespace, env)
    return (name, False)


def unwanted_env_crossing(from_env, to_env):
    if from_env == to_env:
        return False
    if from_env == 'ClusterWide':
        return False
    if to_env == 'ClusterWide':
        return False
    if from_env.startswith(to_env) or to_env.startswith(from_env):
        return False
    if from_env.startswith('sit') and to_env.startswith('sit'):
        return False
    return True


with open('templated-list.yaml', 'r') as f:
    templated = yaml.safe_load(f)
with open('templatable.yaml', 'r') as f:
    templatable = yaml.safe_load(f)

to_do = templated + templatable

service_map = {}
possibly_unwanted_env_crossings = []
incorrect_envs = []
for item in to_do:
    (from_name, from_env) = get_name_env(item, True)
    (to_name, to_env) = get_name_env(item, False)

    if (to_env is False or from_env is False) and from_env != 'ClusterWide' and to_env != 'ClusterWide':
        incorrect_envs.append({
            'from': item['from'],
            'to': item['to'],
            'name': item['name'],
            'to_env': to_env,
            'from_env': from_env,
        })
        continue

    if from_name not in service_map:
        service_map[from_name] = {}

    if unwanted_env_crossing(from_env, to_env):
        possibly_unwanted_env_crossings.append({
            'from_env': from_env,
            'to_env': to_env,
            'from_name': from_name,
            'to_name': to_name,
            'name': item['name']
        })

    if to_name not in service_map[from_name]:
        service_map[from_name][to_name] = set()
    if from_env == 'ClusterWide':
        service_map[from_name][to_name].add(to_env or '')
    else:
        service_map[from_name][to_name].add(from_env)


service_map_without_envs = {}
new_service_map = {}
new_service_map_parseable = {}
for service in service_map:
    service_map_without_envs[service] = list(service_map[service].keys())
    new_service_map_parseable[service] = {}
    displays = []
    for destsvc in service_map[service]:
        displays.append('%s (%s)' % (destsvc, ', '.join(service_map[service][destsvc])))
        new_service_map_parseable[service][destsvc] = list(service_map[service][destsvc])
    new_service_map[service] = displays

    #service_map[service]['destinations'] = list(service_map[service]['destinations'])
    #service_map[service]['envs'] = list(service_map[service]['envs'])
    #service_map[service] = list(service_map[service]['destinations'])
    pass


with open('service-map-with-envs.yaml', 'w') as f:
    yaml.dump(new_service_map, f, indent=2)
with open('service-map-with-envs-parsable.yaml', 'w') as f:
    yaml.dump(new_service_map_parseable, f, indent=2)
with open('service-map.yaml', 'w') as f:
    yaml.dump(service_map_without_envs, f, indent=2, explicit_start=True)
with open('incorrect-envs.yaml', 'w') as f:
    yaml.dump(incorrect_envs, f, indent=2)
with open('env-crossings.yaml', 'w') as f:
    yaml.dump(possibly_unwanted_env_crossings, f, indent=2)
