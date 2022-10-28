#!/usr/bin/python

# This script is intended to be similar to grep for searching the JSON output
# of the scanner.  It uses the JSON output of the scanner and does regex
# searches on the different fields.  It outputs the same format as its input,
# and will preserve any extra fields that have been added.  It supports using
# input and output files, or supports shell style pipes on standard input and
# standard output.

# Usage:
# cat output.json | python3 scripts/grep.py -t amazonaws

import json
import sys
import argparse
import re

data = []
out = []


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout)
parser.add_argument('-n', '--name')
parser.add_argument('-t', '--target')
parser.add_argument('-c', '--check')
parser.add_argument('-d', '--description')

options = parser.parse_args()

re_name = re.compile(options.name) if options.name else re.compile('.*')
re_target = re.compile(options.target) if options.target else re.compile('.*')
re_check = re.compile(options.check) if options.check else re.compile('.*')
if options.description:
    re_description = re.compile(options.description)
else:
    re_description = re.compile('.*')


data = json.load(options.input)

matched = 0

for r in data:
    if re_name.search(r['name']) and re_target.search(r['target']) and re_check.search(r['check']):
        out.append(r)
        matched += 1

# Dump the JSON to standard out, flush sys.stdout to avoid interleving, and
# write a summary.
json.dump(out, options.output, indent=2)
options.output.flush()
sys.stderr.write("Matched %d records\n" % (matched))
