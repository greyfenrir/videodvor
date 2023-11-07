from time import sleep
import logging

from selenium.webdriver.common.by import By


PROJECT_DIR = r'C:\Users\user\Documents\videodvor'
DOWN_DIR = f"{PROJECT_DIR}\\Download"
BUTTON = 'div[contains(@class, "v-button")]'
LOG = logging.getLogger('_d_')
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
            
