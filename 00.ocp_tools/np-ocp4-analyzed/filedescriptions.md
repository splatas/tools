np-ocp4.yaml: original input file

from parse-np (intermediate):
templated.yaml: policies created with given template
non-templated.yaml: policies not created with given template

from parse-np-templated.py:
templated-list.yaml: from/to/name of templated policies
templated-inaccurate: templates where name doesn't match actual environments

parse-np-non-templated.py:
allow-same-namespace.yaml: list of namespaces where allow-same-namespace is allowed
deny-by-default: list of namespaces where deny-by-default is set
templatable.yaml: list of policies that could have been created with the given template but weren't
non-templatable.yaml: list of policies that are "special" and not according to the given template (including some wrong ones)

parse-all-templated.py:
service-map-with-envs.yaml: list of all services and where they communicate to in which envs
service-map-with-envs-parseable.yaml: same as previous, but with ends as an array
service-map.yaml: same syntax as original, but with parsed data
incorrect-envs.yaml: policies that use incorrect styles for environments
incorrect-envs.yaml: parsed policies with environment-crossing traffic





Final files:
templated-inaccurate: templates where name doesn't match actual environments
non-templatable.yaml: list of policies that are "special" and not according to the given template (including some wrong ones)
service-map-with-envs.yaml: list of all services and where they communicate to in which envs
service-map-with-envs-parseable.yaml: same as previous, but with ends as an array
service-map.yaml: same syntax as original, but with parsed data
incorrect-envs.yaml: policies that use incorrect styles for environments
incorrect-envs.yaml: parsed policies with environment-crossing traffic
