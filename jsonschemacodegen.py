from jsonschemacodegen import python as pygen
import yaml

with open('asyncapi.yaml') as fp:
    generator = pygen.GeneratorFromSchema('output_dir')
    generator.Generate(yaml.load(fp), 'Example', 'example')
