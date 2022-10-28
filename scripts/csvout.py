#!/usr/bin/python3

# This script takes JSON input and outputs it as CSV.  This is useful for
# copying the data into spreadsheets to share, etc.

# Usage:
# cat output.json | python scripts/csvout.py -f name -f check -f target -f description

import sys
import argparse
import csv
import json


def value(obj, field):
    return obj[field] if field in obj else ''

parser = argparse.ArgumentParser(description='Get list of records in DSNDB by supplying domains in a JSON file.')
parser.add_argument("-l", "--logging", type=str, default="error",
                    help='enable debugging - levels: info, warning, debug, defaulted to info')
parser.add_argument("input", type=argparse.FileType('r'), nargs='*', default=[sys.stdin])
parser.add_argument("-f", "--field", type=str, action='append')

args = parser.parse_args()

print(args)

# Open the output file
output = csv.writer(sys.stdout)

# Output the header line
fields = list(args.field)
output.writerow(fields)


# Process each input file
for input in args.input:
    js = json.load(input)

    for item in js:
        fields = [value(item, f) for f in args.field]
        output.writerow(fields)