#!/usr/bin/env python3

"""JSON schema to Python3 Classes Generator

Converts JSON schemas, following the definition at https://json-schema.org/, to Python3 class files

Utilises the following packages:

    * JSON-Schema Codegen (https://pypi.org/project/json-schema-codegen/) for code generation
    * PyYAML (https://pypi.org/project/PyYAML/) for YAML parsing

Will process each file in the directory 'schema_dir' with extensions '.json', '.yml' or '.yaml' and produce a Python3 class
file in the directory 'class_dir'.
"""

from jsonschemacodegen import python as pygen
import json
from pydash import py_
import os
import string
import yaml

schema_dir = "../../enviroplusmonitor/schemas"
class_dir  = "../../enviroplusmonitor/classes"

def process_schema(file, schema):
    print("Processing file {file}".format(file=file))
    generator = pygen.GeneratorFromSchema(class_dir)
    generator.Generate(schema=schema, root=None, class_name=py_.capitalize(filename, strict = False), filename_base=filename)


for file in os.listdir(schema_dir):
    filename, extension = os.path.splitext(file)
    if file.endswith(".yml") or file.endswith(".yaml"):
        with open(os.path.join(schema_dir, file)) as fp:
            schema = yaml.load(fp, Loader=yaml.FullLoader)
        process_schema(file, schema)
    elif file.endswith(".json"):
        with open(os.path.join(schema_dir, file)) as fp:
            schema = json.load(fp)
        process_schema(file, schema)
