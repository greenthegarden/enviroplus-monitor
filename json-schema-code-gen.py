from jsonschemacodegen import python as pygen
import yaml

filename = 'asyncapi.yaml'

with open(filename) as fp:
    schema = yaml.load(fp, Loader=FullLoader)
    generator = pygen.GeneratorFromSchema('output_dir')
    generator.Generate(schema=schema, root=None, class_name='Example', filename_base='example')
