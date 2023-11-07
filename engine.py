# coding=utf-8

from time import sleep
from collections import OrderedDict

from selenium.webdriver.common.by import By
from bzt.resources.selenium_extras import waiter, wait_for
import apiritif

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from utils import DOWN_DIR, PROJECT_DIR

from report import ReportBooker, ReportDownloader
from utils import BUTTON, LOG, safe_click


class Engine:
    def __init__(self, ordered_reports):
        timeout = 2.0
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
            "download.default_directory": DOWN_DIR,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False,
            "safebrowsing.disable_download_protection": True
        })
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.set_capability('unhandledPromptBehavior', 'ignore')
        service = Service(log_file=f'{PROJECT_DIR}\\webdriver.log')
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(timeout)
        apiritif.put_into_thread_store(
            timeout=timeout, func_mode=False, driver=self.driver, windows={}, scenario_name='login')        
        self.ordered_reports = ordered_reports
        self.log = LOG
        self.report_booker = ReportBooker(driver=self.driver)
        self.report_downloader = ReportDownloader(driver=self.driver)        

    def get_reports_for_periods(self, company, periods):
        self._login(login=company.login, password=company.password)
        try:
            list_of_rscs = self._get_rscs()
            self.ordered_reports[company.name] = OrderedDict()

            for rsc in list_of_rscs:
                self._set_rsc(rsc)
                self.ordered_reports[company.name][rsc] = list()
                self.report_booker.book(
                    company=company.name,
                    periods=periods,
                    txt_periods=self.ordered_reports[company.name][rsc])

            for rsc in list_of_rscs:
                self._set_rsc(rsc)
                self.report_downloader.get_all_new(
                    company=company.name,
                    txt_periods=self.ordered_reports[company.name][rsc])
        finally:
            self._logout()

    def _logout(self):
        self.log.warning('logout...')
        xpath = f'//{BUTTON}//span[text()="Выход"]/../..'
        safe_click(driver=self.driver, xpath=xpath)
        sleep(1)
        self.log.warning('..done')

    def _login(self, login, password):
        self.driver.get('http://10.54.7.34:7777/ScReportWizard/#!login')
        waiter()
        sleep(3.0)

        login_xpath = '//input[contains(@class, "sc-login-form-user")]'
        pass_xpath = '//input[contains(@class, "sc-login-form-password")]'

        wait_for('visible', [{'xpath': login_xpath}], 20.0)
        self.driver.find_element(By.XPATH, login_xpath).send_keys(login)

        wait_for('visible', [{'xpath': pass_xpath}], 20.0)
        self.driver.find_element(By.XPATH, pass_xpath).send_keys(password)

        enter_button_xpath = f'//{BUTTON}//span[text()="Войти"]/../..'
        wait_for('visible', [{'xpath': enter_button_xpath}], 20.0)
        self.driver.find_element(By.XPATH, enter_button_xpath).click()

    def _get_rscs(self):
        self.log.info('get rscs...')
        # new feature closing xpath: "//div[contains(@class, "v-button-blue-button")]//span[text()="Закрыть"]/../.."
        xpath = '//div[@location="id_2"]//div[@class="v-filterselect-button"]'
        wait_for('clickable', [{'xpath': xpath}], 40)
        rsc_button = self.driver.find_element(By.XPATH, xpath)
        rsc_button.click()
        self.log.info('rsc_button clicked..1')

        elements = self.driver.find_elements(By.XPATH, '//td[contains(@class, "gwt-MenuItem")]')
        rscs = list()
        
        prev_page_xpath = '//div[@class="v-filterselect-prevpage"]/span[text()="Prev"]/..'
        next_page_xpath = '//div[@class="v-filterselect-nextpage"]/span[text()="Next"]/..'
        
        for element in elements:
            span = element.find_element(By.XPATH, './/span')
            rscs.append(span.text)

        rsc_button.click()
        self.log.info(f'rsc_button clicked..2. rscs: {rscs}')
        
        return rscs

    def _set_rsc(self, rsc):
        self.log.info(f'target rsc: "{rsc}"')
        xpath = '//div[@location="id_2"]//div[@class="v-filterselect-button"]'
        wait_for('clickable', [{'xpath': xpath}], 20)
        
        sleep(3)

        rsc_b = self.driver.find_element(By.XPATH, xpath)
        while True:
            rsc_b.click()
            sleep(1.0)            
            xpath = '//td[contains(@class, "gwt-MenuItem")]'
            elements = self.driver.find_elements(By.XPATH, xpath)
            if elements:
                break
        self.log.info(f'len of rscs: {len(elements)}')
        for element in elements:
            # sleep(1)
            span_elements = element.find_elements(By.XPATH, './/span')
            for span in span_elements:                
                if span.text == rsc:
                    self.log.info('rsc found!')
                    element.click()
                    return
                    
        raise Exception(f"RSC '{rsc}' not found")

