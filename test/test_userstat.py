import unittest
import datetime
from pathlib import Path

from internal.yml import read_file_yaml
from userstat.au import get_active_users_from_data_sources, get_file_names


class TestUserStat(unittest.TestCase):
    root_directory = None
    conf = None

    @classmethod
    def setUpClass(cls):
        cls.root_directory = _get_root_directory()
        cls.conf = read_file_yaml(str(TestUserStat.root_directory)+"/data/userstat/userstat.yml")

    def test_user_stat_wau(self):
        at_date = datetime.datetime(2024, 12, 9)
        report = create_report(at_date, days=7)
        self.assertEqual(len(report['users']), 5)
        self.assertEqual(len(report['users']['3']), 8)

    def test_user_stat_dau_timeslots(self):
        at_date = datetime.datetime(2024, 12, 9)
        report = create_report(at_date, days=1, timeslots=True)
        self.assertEqual(len(report['users']), 3)
        self.assertEqual(report['timeslots'][12], 3)
        # self.assertEqual(len(report['timeslots'][14]), 2)
        # self.assertEqual(len(report['timeslots'][15]), 2)

def create_report(dt: datetime.datetime, timeslots=False, days=1):
    return get_active_users_from_data_sources(
        get_file_names(
            dt,
            root_dir=str(TestUserStat.root_directory),
            template=TestUserStat.conf['fileNameTemplate'],
            days=days),
        with_timeslots=timeslots,
        pattern=TestUserStat.conf['sourceFormat'],
        entry_keys=TestUserStat.conf['entryKeys']
    )

def _get_root_directory() -> Path:
    return Path(__file__).parent.parent


if __name__ == '__main__':
    unittest.main()
