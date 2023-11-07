import os

from time import sleep
import logging

from selenium.webdriver.common.by import By

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
DOWN_DIR = os.path.join(f"{PROJECT_DIR}", "Download")
BUTTON = 'div[contains(@class, "v-button")]'

LOG = logging.getLogger('_d_')
LOG.setLevel(logging.INFO)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
fileHandler = logging.FileHandler("{0}/{1}.log".format(PROJECT_DIR, "just_log"))
fileHandler.setFormatter(logFormatter)
LOG.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
LOG.addHandler(consoleHandler)


MONTHS = ['ЯНВАРЬ', 'ФЕВРАЛЬ', 'МАРТ', 'АПРЕЛЬ', 'МАЙ', 'ИЮНЬ',
          'ИЮЛЬ', 'АВГУСТ', 'СЕНТЯБРЬ', 'ОКТЯБРЬ', 'НОЯБРЬ', 'ДЕКАБРЬ']


def safe_click(driver, xpath, step_limit=5):
    step = 0
    while True:
        try:
            driver.find_element(By.XPATH, xpath).click()
            return
        except Exception as exc:
            step += 1
            LOG.warning(f'{exc}\ntry again to click "{xpath}"[{step}')
            sleep(1)
            if step > step_limit:
                raise exc
            
