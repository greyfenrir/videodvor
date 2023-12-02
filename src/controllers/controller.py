# coding=utf-8

from time import sleep, time
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as econd
from selenium.webdriver.common.by import By

from utils import LOG


class WebController:
    BUTTON = 'div[contains(@class, "v-button")]'

    def __init__(self, driver):
        self.driver = driver
        self.log = LOG
        self.default_timeout = 40

    def waiter(self):
        try:
            script = 'return document.readyState'
            msg = "Timeout occurred while waiting for page to finish loading."
            WebDriverWait(self.driver, self.default_timeout).until(
                lambda drv: drv.execute_script(script) == 'complete', message=msg)
        except UnexpectedAlertPresentException:
            pass

    def wait_for(self, condition, xpath, timeout):
        def get_until_cond():
            if "clickable" in condition:
                return econd.element_to_be_clickable(locator)
            if "present" in condition:
                return econd.presence_of_element_located(locator)
            if "visible" in condition:
                return econd.visibility_of_element_located(locator)

        start_time = time()
        while True:
            locator = By.XPATH, xpath
            element = None
            try:
                element = WebDriverWait(self.driver, timeout).until(get_until_cond())
            except TimeoutException:
                pass
            if element:
                return element

            elapsed_time = time() - start_time
            if elapsed_time > timeout:
                raise NoSuchElementException("Timeout occurred while waiting for '%s' condition" % condition)

    def safe_send(self, xpath, text, step_limit=5):
        step = 0
        while True:
            try:
                self.driver.find_element(By.XPATH, xpath).send_keys(text)
                return
            except Exception as exc:
                step += 1
                LOG.warning(f'{exc}\ntry again to send "{text}"[{step}')
                sleep(3)
                if step > step_limit:
                    raise exc

    def safe_click(self, xpath, step_limit=5):
        step = 0
        while True:
            try:
                self.driver.find_element(By.XPATH, xpath).click()
                return
            except Exception as exc:
                step += 1
                LOG.warning(f'{exc}\ntry again to click "{xpath}"[{step}')
                sleep(1)
                if step > step_limit:
                    raise exc
