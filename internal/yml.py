import yaml
from internal.exception import APITesterIOException


def read_file_yaml(fname):
    with open(fname, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise APITesterIOException("Failed to read {0} due to an parsing error: {1}".format(fname, exc))
        except Exception as e:
            raise APITesterIOException("Failed to read {0}: {1}".format(fname, e))



def write_file_yaml(fname, d):
    try:
        with open(fname, 'w') as stream:
            yaml.dump(d, stream, default_flow_style=False)
    except yaml.YAMLError as exc:
        raise APITesterIOException("Failed to write {0} due to an yaml error: {1}".format(fname, exc))
    except Exception as e:
        raise APITesterIOException("Failed to write {0}: {1}".format(fname, e))
