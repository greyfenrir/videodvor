# coding=utf-8
import time
from selenium.webdriver.common.by import By

from controllers.controller import WebController
from utils import MONTHS


class ReportBooker(WebController):
    def book(self, company, periods, txt_periods):
        self._choose_report(company=company)
        self._order_reports(company=company, periods=periods, txt_periods=txt_periods)

    def _order_reports(self, company, periods, txt_periods):
        for month, year in periods:
            interval = self._run_report(company, month, year)

            if interval:
                txt_periods.append(interval)  # '08.2023'
                self.log.info(f'target interval for renaming: "{interval}"')

    def _run_report(self, company, month, year):
        # open report execution dialog
        run_xpath = f'//{self.BUTTON}//span[text()="Выполнить"]/../..'
        self.wait_for('clickable', run_xpath, 20)
        self.log.warning(f'run_report({company}, {month}, {year})')
        self.safe_click(run_xpath)

        # choose interval
        self._set_interval(month, year)  # 'ИЮЛЬ 2023'

        # push execute button
        execute_button_xpath = f'//div[@class="popupContent"]//{self.BUTTON}//span[text()="Выполнить"]/../..'
        self.wait_for('clickable', execute_button_xpath, 20)
        if len(self.driver.find_elements(By.XPATH, execute_button_xpath)) > 1:
            self.log.warning('more than one execute button found!')

        self.driver.find_element(By.XPATH, execute_button_xpath).click()
        self.log.warning('execute button pressed successfully')

        num_interval = f'{month:02d}.{year}'
        return num_interval

    def _set_interval(self, month, year):
        self.log.info(f'set_interval("{month}, {year}"):')
        txt_interval = f'{MONTHS[month - 1]} {year}'

        # click on dropdown..
        dropdown_xpath = '//div[contains(@class, "v-filterselect-month-db-selector")]'
        self.safe_click(xpath=dropdown_xpath)
        self.log.warning('selector clicked')

        # find line in dropdown and click on it
        prev_xpath = '//div[contains(@class, "v-filterselect-prevpage")]/span[text()=="Prev"]/..'
        next_xpath = '//div[contains(@class, "v-filterselect-nextpage")]/span[text()=="Next"]/..'
        while True:
            time.sleep(1)
            span_xpath = f'//td[contains(@class, "gwt-MenuItem")]/span[contains(text(),"20"]'
            spans = self.driver.find_elements(By.XPATH, span_xpath)
            self.log.info(f'len spans for {txt_interval}: {len(spans)}')
            current_year = spans[0].text.split(' ')[1]
            if current_year < year:
                self.log.info(f'{current_year} found, go forward')
                self.safe_click(xpath=prev_xpath)
            elif current_year > year:
                self.log.info(f'{current_year} found, go backward')
                self.safe_click(xpath=next_xpath)
            else:
                self.log.info(f'{year} found successfully')
                break   # page with target interval found

        interval_xpath = f'//td[contains(@class, "gwt-MenuItem")]/span[text()="{txt_interval}"]/..'

        self.wait_for('clickable', interval_xpath, 20)
        self.driver.find_element(By.XPATH, interval_xpath).click()
        self.log.warning('interval chosen!')

    def _choose_report(self, company):
        search_panel = 'div[contains(@class, "sc-filter-panel-layout")]'
        search_field = 'input[contains(@class, "sc-filter-panel-field")]'
        search_button = 'div[contains(@class, "sc-filter-panel-button")]'

        # input company name
        self.log.warning("waiting for input line...")
        input_line_xpath = f"//{search_panel}/{search_field}"
        self.wait_for('visible', input_line_xpath, 60)
        
        self.log.warning(f'input company name..({input_line_xpath})')
        self.safe_send(xpath=input_line_xpath, text=company)
        self.log.warning('done')

        # click 'find' button
        self.log.warning('click find button..')
        find_button_xpath = f"//{search_panel}/{search_button}"
        self.log.warning(f"find button xpath: {find_button_xpath}")
        self.wait_for('clickable', find_button_xpath, 20)
        self.driver.find_element(By.XPATH, find_button_xpath).click()

        target_span_xpath = f'//div[contains(@class, "v-tree-node-leaf")]//span[contains(text(), "{company}")]'
        self.log.warning(f'target_span_xpath: {target_span_xpath}')
        self.wait_for('visible', target_span_xpath, 20)
        target_span = self.driver.find_element(By.XPATH, target_span_xpath)

        rsc = target_span.text.split(' ')[-1]
        self.log.warning(f'short rsc found: {rsc}')

        # choose target report
        target_span.find_element(By.XPATH, './..').click()


