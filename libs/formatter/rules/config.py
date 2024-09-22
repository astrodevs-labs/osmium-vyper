import os
import tomli

rules_types = [
    { "field": "indentation", "type": int, "default": 4 }
]

def init_config(root, config_file):
    if config_file is None:
        config_file = os.path.join(root, 'vyfmt.toml')

    config = {}
    modified_fields = []
    if os.path.exists(config_file):
        with open(config_file) as reader:
            content = reader.read()
            parsed_file = tomli.loads(content)

            for rule in rules_types:
                field = rule["field"]
                if field in parsed_file:
                    if type(parsed_file[field]) != rule["type"]:
                        raise TypeError(f"Field '{field}' in configuration file is not of type '{rule['type']}'")
                    else:
                        config[field] = parsed_file[field]
                        modified_fields.append(field)

    for rule in rules_types:
        field = rule["field"]
        if field not in modified_fields:
            config[field] = rule["default"]

    return config






