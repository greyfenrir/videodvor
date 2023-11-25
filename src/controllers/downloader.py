# coding=utf-8

import os
from time import sleep

from selenium.webdriver.common.by import By

from controllers.controller import WebController
from utils import DOWN_DIR, SORT_DIR


class ReportDownloader(WebController):
    def __init__(self, driver):
        super().__init__(driver=driver)
        self.ordered_list = None
        self.company = None
        # self._clean_sort_dir()

    @staticmethod
    def _get_block_xpath(name, postfix='/../../..//div[@class="v-slot"]'):
        report_win = 'div[contains(@class, "v-popupbutton-popup")]'
        block_xpath = '//{rep_win}//span[text()="{span_text}"]'
        return block_xpath.format(rep_win=report_win, span_text=name)+postfix

    def _clean_down_dir(self):
        self.log.warning('start cleaning..')
        downloaded_files = [os.path.join(f"{DOWN_DIR}", f"{f}")
                            for f in os.listdir(path=DOWN_DIR) if f.startswith(self.company)]
        if downloaded_files:
            self.log.warning(f'Clean downloaded files: {downloaded_files}')
            for f in downloaded_files:
                self.log.warning(f'try to remove "{f}"..')
                os.remove(f)
            self.log.warning(f'done. dir: {os.listdir(path=DOWN_DIR)}')

    def _clean_sort_dir(self):
        sorted_files = [os.path.join(f"{SORT_DIR}", f"{f}")
                        for f in os.listdir(path=SORT_DIR)]
        if sorted_files:
            self.log.warning(f'Remove sorted files: {sorted_files}')
            for f in sorted_files:
                os.remove(f)

    def _clean_executed_elements(self):
        executed_xpath = self._get_block_xpath("Выполненные")
        while True:
            sleep(1.0)
            executed_elements = self.driver.find_elements(By.XPATH, executed_xpath)
            if not executed_elements:
                self.log.info('no executed elements')
                break
            # remove first element..
            self.log.info(f'remove {executed_elements[0]}..')
            executed_elements[2].click()

    def _clean_new_elements(self):
        new_xpath = self._get_block_xpath("Новые")
        while True:
            sleep(1.0)
            new_elements = self.driver.find_elements(By.XPATH, new_xpath)
            if not new_elements:
                self.log.info('no new elements')
                break
            # remove first element..
            self.log.info(f'remove {new_elements[0]}..')
            new_elements[2].click()

    def _download_new_elements(self):
        self._clean_down_dir()

        new_xpath = self._get_block_xpath("Новые")
        while True:            
            sleep(1.0)
            new_elements = self.driver.find_elements(By.XPATH, new_xpath)
            if not (self.ordered_list and new_elements):
                self.log.info('end of downloading')
                break
            else:
                self.log.info(f'len(new_elements): {len(new_elements)}')

            self.log.warning('click on new element...')
            new_elements[0].click()

            self._rename_file_when_ready()

    def _rename_file_when_ready(self):
        while True:
            self.log.info('waiting for file...')
            downloaded_files = [
                f for f in os.listdir(path=DOWN_DIR) if
                f.startswith(self.company) and not f.endswith('crdownload')]
            if downloaded_files:
                if len(downloaded_files) > 1:
                    self.log.warning(f'strange downloaded files: {downloaded_files}')
                self.log.warning(f'downloaded files: {downloaded_files}')
                break
            sleep(1.0)

        old_name = downloaded_files[0]  # НВА_ГОМ..xlsx
        name_parts = old_name.split('.')
        period = self.ordered_list.pop()  # '08.2023'
        new_name = f"{name_parts[0]}.{period}.{name_parts[2]}"  # НВА_ГОМ.08.2023.xlsx
        full_old_name = os.path.join(DOWN_DIR, f"{old_name}")
        full_new_name = os.path.join(SORT_DIR, f"{new_name}")
        self.log.info(f'full_old_name: {full_old_name}, full_new_name: {full_new_name}')
        os.rename(full_old_name, full_new_name)

    def _wait_for_readiness(self):
        queue_xpath = self._get_block_xpath("Очередь на выполнение", postfix='')
        running_xpath = self._get_block_xpath("Выполняемые", postfix='')

        while True:
            queue = self.driver.find_elements(By.XPATH, queue_xpath)
            execution = self.driver.find_elements(By.XPATH, running_xpath)
            pending_list = []
            if not queue and not execution:
                self.log.warning('all reports are ready')
                break
            if queue:
                pending_list.append('queue')
            if execution:
                pending_list.append('execution')
            self.log.warning(f'{", ".join(pending_list)} found. Waiting for reports...')
            sleep(5.0)

    def _open_report_window(self):
        report_button_xpath = f'//{self.BUTTON}//span[contains(text(), "Отчеты (")]/../..'
        sleep(1.0)
        self.log.info('trying to open report window..')
        self.wait_for('clickable', report_button_xpath, 60)
        if len(self.driver.find_elements(By.XPATH, report_button_xpath)) > 1:
            self.log.warning('more than one report_button found!')
        self.log.info('trying to click..')
        self.driver.find_element(By.XPATH, report_button_xpath).click()
        self.log.info('done!')

    def _close_report_window(self):
        self._open_report_window()

    def remove_all_new(self):
        self._open_report_window()
        self._clean_new_elements()
        self._close_report_window()

    def get_all_new(self, company, txt_periods):
        self.ordered_list = txt_periods
        self.company = company

        self._open_report_window()

        self._wait_for_readiness()
        self._download_new_elements()
        self._clean_executed_elements()

        self._close_report_window()
