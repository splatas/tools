#!/usr/bin/python3
import sys

import yaml

with open(sys.argv[1], 'r') as f:
    parsed = yaml.safe_load(f)

print(parsed)
