import logging
import os
import yaml

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DOWN_DIR = os.path.join(f"{PROJECT_DIR}", "Download")
SORT_DIR = os.path.join(f"{PROJECT_DIR}", "reports")

LOG = logging.getLogger('')
LOG.setLevel(logging.INFO)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
fileHandler = logging.FileHandler("{0}/{1}.log".format(PROJECT_DIR, "just_log"))
fileHandler.setFormatter(logFormatter)
LOG.addHandler(fileHandler)


LOG.info(f'PROJECT_DIR: "{PROJECT_DIR}"')
LOG.info(f'DOWN_DIR: "{DOWN_DIR}"')
LOG.info(f'SORT_DIR: "{SORT_DIR}"')

MONTHS = ['ЯНВАРЬ', 'ФЕВРАЛЬ', 'МАРТ', 'АПРЕЛЬ', 'МАЙ', 'ИЮНЬ',
          'ИЮЛЬ', 'АВГУСТ', 'СЕНТЯБРЬ', 'ОКТЯБРЬ', 'НОЯБРЬ', 'ДЕКАБРЬ']


def get_periods(start_p, end_p):
    periods = []
    first_m, first_y = [int(part) for part in start_p.split('.')]
    last_m, last_y = [int(part) for part in end_p.split('.')]
    periods.append((first_m, first_y))
    while not (first_m == last_m and first_y == last_y):
        first_m += 1
        if first_m > 12:
            first_m = 1
            first_y += 1

        periods.append((first_m, first_y))
    return periods


class Configuration:
    config_path = os.path.join(PROJECT_DIR, 'config.yaml')

    def __init__(self):
        self.companies = dict()
        self.periods = '02.2023', '04.2023'
        self.read_config()

    def read_config(self):
        with open(self.config_path, 'r+', encoding='utf-8') as config_file:
            config = yaml.safe_load(config_file.read())

        self.companies = config.get('configuration').get('clients')


