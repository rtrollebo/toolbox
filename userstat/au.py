"""
Module for generating active users statistics

"""
import re
import datetime
import platform

from internal.io import read_file


def add_param_to_stat(par: int, slots: dict) -> bool:
    if par not in slots:
        slots[par] = 1
    else:
        slots[par] = slots[par]+1

def get_active_users(s, report: dict, with_timeslots=False, pattern="", entry_keys=None):
    """

    :param s:
    :param report:
    :param with_timeslots:
    :param pattern:
    :param entry_keys:
    :return:
    """
    if entry_keys is None:
        entry_keys = ["userId"]
    nlines = 0
    if platform.system() == 'Windows':
        # linerange = s.splitlines() # TODO: for test case
        linerange = s.split('\\n') # FOR actual windows intput files
    else:
        # Assume unix-compatible system
        linerange = s.split('\\n')
        # linerange = s.splitlines()
    for line in linerange:
        r = re.findall(pattern, line)
        if len(r) != 0:
            userid = r[0][7]
            hour = int(r[0][4])
            minute = int(r[0][5])
            second = int(r[0][6])
            entry = {}
            for i, value in enumerate(entry_keys):
                entry[value] = r[0][7+i]
            entry['time'] = datetime.datetime(int(r[0][3]), to_month[r[0][2]], int(r[0][1]), hour, minute, second)
            if userid not in report['users']:
                report['users'][userid] = [entry]
                if with_timeslots:
                    add_param_to_stat(hour, report['timeslots'])
            else:
                report['users'][userid].append(entry)
        nlines = nlines + 1
    return report['users'], report['timeslots']

def get_active_users_from_data_sources(data_sources: list, pattern="", entry_keys=None):
    if entry_keys is None:
        entry_keys = ["userId"]
    active_users_report = {'users': {}, 'timeslots': {}}
    for file in data_sources:
        d = read_file(file)
        get_active_users(str(d), active_users_report, with_timeslots=True, pattern=pattern, entry_keys=entry_keys)
    return active_users_report

def get_file_names(dt: datetime.datetime, root_dir ="", template="", days=7) -> list:
    """

    :param dt:
    :param root_dir:
    :param template:
    :param days:
    :return:
    """
    if root_dir is not None or root_dir != "":
        if root_dir[-1] != "/":
            root_dir = root_dir + "/"
    dts = [dt - datetime.timedelta(days=i) for i in range(0, days)]
    return [root_dir+template.format(i.date().isoformat()) for i in dts]

to_month = {
    'Jan': 1,
    'Feb': 2,
    'Mar' : 3,
    'Apr': 4,
    'Mai': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug':8,
    'Sep':9,
    'Oct':10,
    'Nov':11,
    'Dec':12}


