import yaml

with open("./src/data_config.yml", 'r') as stream:
    try:
        VALIDATION_CONFIGURATION = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)