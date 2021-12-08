import json

from jsonpath_ng import jsonpath, parse

with open("scripts/api_tests_generator/examples/invoices.json", "r") as json_file:
    json_data = json.load(json_file)

jsonpath_expression = parse("[*].id")

for match in jsonpath_expression.find(json_data):
    print(f"Type: {match.value}")
