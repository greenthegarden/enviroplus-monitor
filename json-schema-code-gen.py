#!/usr/bin/env python3

from jsonschemacodegen import python as pygen
import yaml

filename = 'schemas/configPayload.yaml'

with open(filename) as fp:
    schema = yaml.load(fp, Loader=yaml.FullLoader)
    generator = pygen.GeneratorFromSchema('output_dir')
    generator.Generate(schema=schema, root=None, class_name='Example', filename_base='example')
