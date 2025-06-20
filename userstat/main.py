import sys
import userstat.au as au
from internal.yml import read_file_yaml
from internal.io import get_root_directory


def py_version_up_to_date() -> bool:
    return sys.version_info.major >= 3 and sys.version_info.minor >= 10

def main(*args):
    if not py_version_up_to_date():
        raise Exception("Requires Python version 3.10 or higher")
    if len(args) < 3:
        raise NameError("Required arguments: <path to dat> <datetime of active users> <days>")
    root_dir = get_root_directory()
    conf = read_file_yaml(str(root_dir) + "/data/userstat/userstat.yml")
    return au.get_active_users_from_data_sources(
        au.get_file_names(
            args[1],
            root_dir=str(root_dir),
            template=conf['fileNameTemplate'],
            days=args[2]),
        with_timeslots=False,
        pattern=conf['sourceFormat'],
        entry_keys=conf['entryKeys']
    )