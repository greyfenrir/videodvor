# coding=utf-8

from time import sleep

import os
from selenium.webdriver.common.by import By

from utils import BUTTON, LOG, DOWN_DIR, MONTHS, safe_click, wait_for


class ReportBooker:
    def __init__(self, driver):
        self.driver = driver
        self.log = LOG

    def book(self, company, periods, txt_periods):
        self._choose_report(company=company)
        self._order_reports(company=company, periods=periods, txt_periods=txt_periods)

    def _order_reports(self, company, periods, txt_periods):
        for month, year in periods:
            self._run_report(company, month, year)

            target_interval = f'{month:02d}.{year}'
            txt_periods.append(target_interval)  # '08.2023'

            self.log.warning(f'target interval for renaming: "{target_interval}"')

    def _run_report(self, company, month, year):
        # open report execution dialog
        run_xpath = f'//{BUTTON}//span[text()="Выполнить"]/../..'
        wait_for('clickable', [{'xpath': run_xpath}], 20.0)
        self.log.warning(f'run_report({company}, {month}, {year})')
        safe_click(self.driver, run_xpath)

        # choose interval
        target_interval = f'{MONTHS[month - 1]} {year}'
        self.log.warning(f'target report interval: "{target_interval}"')
        self._set_interval(target_interval)  # 'ИЮЛЬ 2023'

        # push execute button
        execute_button_xpath = f'//div[@class="popupContent"]//{BUTTON}//span[text()="Выполнить"]/../..'
        wait_for('clickable', [{'xpath': execute_button_xpath}], 20.0)
        if len(self.driver.find_elements(By.XPATH, execute_button_xpath)) > 1:
            self.log.warning('more than one execute button found!')

        self.driver.find_element(By.XPATH, execute_button_xpath).click()
        self.log.warning('execute button pressed successfully')

    def _set_interval(self, interval):
        # click on dropdown..
        self.log.info(f'set_interval("{interval}"):')

        dropdown_xpath = '//div[contains(@class, "v-filterselect-month-db-selector")]'
        # wait_for('clickable', [{'xpath': dropdown_xpath}], 20.0)
        # self.driver.find_element(By.XPATH, dropdown_xpath).click()
        safe_click(driver=self.driver, xpath=dropdown_xpath)
        self.log.warning('selector clicked')

        # find line in dropdown and click on it
        interval_xpath = f'//td[contains(@class, "gwt-MenuItem")]/span[text()="{interval}"]/..'
        wait_for('clickable', [{'xpath': interval_xpath}], 20.0)
        target_interval = self.driver.find_element(By.XPATH, interval_xpath)
        target_interval.click()
        self.log.warning('interval chosen!')

    def _choose_report(self, company):
        search_panel = 'div[contains(@class, "sc-filter-panel-layout")]'
        search_field = 'input[contains(@class, "sc-filter-panel-field")]'
        search_button = 'div[contains(@class, "sc-filter-panel-button")]'

        # input company name
        self.log.warning("waiting for input line...")
        input_line_xpath = f"//{search_panel}/{search_field}"
        wait_for('visible', [{'xpath': input_line_xpath}], 40.0)

        sleep(3)

        wait_for('visible', [{'xpath': input_line_xpath}], 40.0)
        self.log.warning(f'input company name..({input_line_xpath})')
        self.driver.find_element(By.XPATH, input_line_xpath).send_keys(company)
        self.log.warning('done')

        # click 'find' button
        self.log.warning('click find button..')
        find_button_xpath = f"//{search_panel}/{search_button}"
        self.log.warning(f"find button xpath: {find_button_xpath}")
        wait_for('clickable', [{'xpath': find_button_xpath}], 20.0)
        self.driver.find_element(By.XPATH, find_button_xpath).click()

        target_span_xpath = f'//div[contains(@class, "v-tree-node-leaf")]//span[contains(text(), "{company}")]'
        self.log.warning(f'target_span_xpath: {target_span_xpath}')
        wait_for('visible', [{'xpath': target_span_xpath}], 20.0)
        target_span = self.driver.find_element(By.XPATH, target_span_xpath)

        rsc = target_span.text.split(' ')[-1]
        self.log.warning(f'short rsc found: {rsc}')

        # choose target report
        target_span.find_element(By.XPATH, './..').click()


class ReportDownloader:
    def __init__(self, driver):
        self.driver = driver
        self.ordered_list = None
        self.company = None
        self.download_dir = DOWN_DIR
        self.log = LOG
        self._clean_sort_dir()

    @staticmethod
    def _get_block_xpath(name, postfix='/../../..//div[@class="v-slot"]'):
        report_win = 'div[contains(@class, "v-popupbutton-popup")]'
        block_xpath = '//{rep_win}//span[text()="{span_text}"]'
        return block_xpath.format(rep_win=report_win, span_text=name)+postfix

    def _clean_down_dir(self):
        self.log.warning('start cleaning..')
        downloaded_files = [os.path.join(f"{self.download_dir}", f"{f}")
                            for f in os.listdir(path=self.download_dir) if f.startswith(self.company)]
        if downloaded_files:
            self.log.warning(f'Clean downloaded files: {downloaded_files}')
            for f in downloaded_files:
                self.log.warning(f'try to remove "{f}"..')
                os.remove(f)
            self.log.warning(f'done. dir: {os.listdir(path=self.download_dir)}')

    def _clean_sort_dir(self):
        sorted_path = os.path.join(self.download_dir, 'sorted')
        sorted_files = [os.path.join(f"{sorted_path}", f"{f}")
                        for f in os.listdir(path=sorted_path)]
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
            self.log.warning('_download_new_elements whileTrue:')
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
            downloaded_files = [
                f for f in os.listdir(path=self.download_dir) if
                f.startswith(self.company) and not f.endswith('crdownload')]
            if downloaded_files:
                if len(downloaded_files) > 1:
                    self.log.warning(f'strange downloaded files: {downloaded_files}')
                break
            sleep(1.0)

        self.log.warning(f'downloaed_files: {downloaded_files}')
        old_name = downloaded_files[0]  # НВА_ГОМ..xlsx
        self.log.warning(f'old_name: {old_name}')
        name_parts = old_name.split('.')
        self.log.warning(f'name_parts: {name_parts}')
        period = self.ordered_list.pop()  # '08.2023'
        self.log.warning(f'period: {period} ({len(self.ordered_list)} are rest)')
        new_name = f"{name_parts[0]}.{period}.{name_parts[2]}"  # НВА_ГОМ.08.2023.xlsx
        self.log.warning(f'new_name: {new_name}')
        os.rename(f"Download\\{old_name}", f"Download\\sorted\\{new_name}")

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
        report_button_xpath = f'//{BUTTON}//span[contains(text(), "Отчеты (")]/../..'
        sleep(1.0)
        self.log.info('trying to open report window..')
        wait_for('clickable', [{'xpath': report_button_xpath}], 40.0)
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
