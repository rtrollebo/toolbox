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
        cls.root_directory = get_root_directory()
        cls.conf = read_file_yaml(str(TestUserStat.root_directory)+"/data/userstat/userstat.yml")

    def test_user_stat(self):
        at_date = datetime.datetime(2024, 12, 9)
        report = get_active_users_from_data_sources(
            get_file_names(
                at_date,
                root_dir=str(TestUserStat.root_directory),
                template=TestUserStat.conf['fileNameTemplate'],
                days=7),
            pattern=TestUserStat.conf['sourceFormat'],
            entry_keys=TestUserStat.conf['entryKeys']
        )
        self.assertEqual(len(report['users']), 5)
        self.assertEqual(len(report['users']['3']), 8)

def get_root_directory() -> Path:
    return Path(__file__).parent.parent


if __name__ == '__main__':
    unittest.main()
