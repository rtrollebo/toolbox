import yaml


def read_file_yaml(fname):
    with open(fname, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def write_file_yaml(fname, d):
    try:
        with open(fname, 'w') as stream:
            yaml.dump(d, stream, default_flow_style=False)
    except yaml.YAMLError as exc:
        print("problem")
