import logging
import os

PROJECT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
DOWN_DIR = os.path.join(f"{PROJECT_DIR}", "Download")
SORT_DIR = os.path.join(f"{PROJECT_DIR}", "reports")

LOG = logging.getLogger('')
LOG.setLevel(logging.INFO)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
fileHandler = logging.FileHandler("{0}/{1}.log".format(PROJECT_DIR, "just_log"))
fileHandler.setFormatter(logFormatter)
LOG.addHandler(fileHandler)


MONTHS = ['ЯНВАРЬ', 'ФЕВРАЛЬ', 'МАРТ', 'АПРЕЛЬ', 'МАЙ', 'ИЮНЬ',
          'ИЮЛЬ', 'АВГУСТ', 'СЕНТЯБРЬ', 'ОКТЯБРЬ', 'НОЯБРЬ', 'ДЕКАБРЬ']