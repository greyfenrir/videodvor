# coding=utf-8
import os.path
from time import sleep
from collections import OrderedDict
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from controllers.booker import ReportBooker
from controllers.downloader import ReportDownloader
from controllers.login import Login
from utils import DOWN_DIR, PROJECT_DIR, LOG


class Engine:
    def __init__(self, ordered_reports):
        timeout = 2.0
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
            "download.default_directory": "C:\\Users\\user\\Documents\\videodvor",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False,
            "safebrowsing.disable_download_protection": True
        })
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.set_capability('unhandledPromptBehavior', 'ignore')
        log_path = os.path.join(f'{PROJECT_DIR}', 'webdriver.log')
        service = Service(log_file=log_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(timeout)

        self.manager = Login(self.driver, ordered_reports)
        self.report_booker = ReportBooker(driver=self.driver)
        self.report_downloader = ReportDownloader(driver=self.driver)        

    def get_reports_for_periods(self, company, periods):
        self.manager.login(login=company.login, password=company.password)
        try:
            list_of_rscs = self.manager.get_rscs()
            self.manager.ordered_reports[company.name] = OrderedDict()

            for rsc in list_of_rscs:
                self.manager.set_rsc(rsc)
                self.manager.ordered_reports[company.name][rsc] = list()
                self.report_booker.book(
                    company=company.name,
                    periods=periods,
                    txt_periods=self.manager.ordered_reports[company.name][rsc])

            for rsc in list_of_rscs:
                self.manager.set_rsc(rsc)
                self.report_downloader.get_all_new(
                    company=company.name,
                    txt_periods=self.manager.ordered_reports[company.name][rsc])

        finally:
            self.manager.logout()
            self.driver.quit()
