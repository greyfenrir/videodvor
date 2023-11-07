import os
import time
from time import sleep
import logging

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as econd

PROJECT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
DOWN_DIR = os.path.join(f"{PROJECT_DIR}", "Download")
SORT_DIR = os.path.join(f"{PROJECT_DIR}", "reports")

BUTTON = 'div[contains(@class, "v-button")]'

LOG = logging.getLogger('')
LOG.setLevel(logging.INFO)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
fileHandler = logging.FileHandler("{0}/{1}.log".format(PROJECT_DIR, "just_log"))
fileHandler.setFormatter(logFormatter)
LOG.addHandler(fileHandler)


MONTHS = ['ЯНВАРЬ', 'ФЕВРАЛЬ', 'МАРТ', 'АПРЕЛЬ', 'МАЙ', 'ИЮНЬ',
          'ИЮЛЬ', 'АВГУСТ', 'СЕНТЯБРЬ', 'ОКТЯБРЬ', 'НОЯБРЬ', 'ДЕКАБРЬ']


def waiter(driver, timeout):
    try:
        script = 'return document.readyState'
        msg = "Timeout occurred while waiting for page to finish loading."
        WebDriverWait(driver, timeout).until(lambda drv: drv.execute_script(script) == 'complete', message=msg)
    except UnexpectedAlertPresentException:
        pass


def wait_for(driver, condition, xpath, wait_timeout):
    def get_until_cond():
        if "clickable" in condition:
            return econd.element_to_be_clickable(locator)
        if "present" in condition:
            return econd.presence_of_element_located(locator)
        if "visible" in condition:
            return econd.visibility_of_element_located(locator)

    start_time = time.time()
    while True:
        locator = By.XPATH, xpath
        element = None
        try:
            element = WebDriverWait(driver, wait_timeout).until(get_until_cond())
        except TimeoutException:
            pass
        if element:
            return element

        elapsed_time = time.time() - start_time
        if elapsed_time > wait_timeout:
            raise NoSuchElementException("Timeout occurred while waiting for '%s' condition" % condition)


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
