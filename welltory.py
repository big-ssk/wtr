import os
import json
from jsonschema import Draft7Validator, RefResolver


def validate(path):
    json_dir = os.path.join(path, 'event')
    json_files = os.listdir(json_dir)
    schema_dir = os.path.join(path, 'schema')
    schema_files = os.listdir(schema_dir)

    for schema_filename in schema_files:
        for json_filename in json_files:
            with open(os.path.join(schema_dir, schema_filename)) as json_schema, \
                    open(os.path.join(json_dir, json_filename)) as json_data:
                schema = json.load(json_schema)
                data = json.load(json_data)

                Draft7Validator.check_schema(schema)
                resolver = RefResolver(schema_dir, schema)
                validator = Draft7Validator(schema, resolver=resolver)

                yield validator.iter_errors(data)


with open('README.md', 'w') as file:
    for instance in validate(os.getcwd()):
        for error in instance:
            try:
                message = f"File: {error.instance['id']}.json. Error: {error.message}. " \
                          f"Schema: {error.instance['event']}.schema"
                print(message, end='\n', file=file)
            except (TypeError, KeyError):
                pass
