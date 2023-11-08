# coding=utf-8

from time import sleep

from selenium.webdriver.common.by import By

from controllers.controller import WebController


class Login(WebController):
    def __init__(self, driver, ordered_reports):
        super().__init__(driver)
        self.ordered_reports = ordered_reports

    def logout(self):
        self.log.warning('logout...')
        xpath = f'//{self.BUTTON}//span[text()="Выход"]/../..'
        self.safe_click(xpath=xpath)
        sleep(1)
        self.log.warning('..done')

    def login(self, login, password):
        self.driver.get('http://10.54.7.34:7777/ScReportWizard/#!login')
        self.waiter()
        sleep(3.0)

        login_xpath = '//input[contains(@class, "sc-login-form-user")]'
        pass_xpath = '//input[contains(@class, "sc-login-form-password")]'

        self.wait_for('visible', login_xpath, 20)
        self.driver.find_element(By.XPATH, login_xpath).send_keys(login)

        self.wait_for('visible', pass_xpath, 20)
        self.driver.find_element(By.XPATH, pass_xpath).send_keys(password)

        enter_button_xpath = f'//{self.BUTTON}//span[text()="Войти"]/../..'
        self.wait_for('visible', enter_button_xpath, 20)
        self.driver.find_element(By.XPATH, enter_button_xpath).click()

    def _close_new_feature_notification(self):
        # new feature closing xpath:
        xpath = '//div[contains(@class, "v-button-blue-button")]//span[text()="Закрыть"]/../..'
        notifications = self.driver.find_elements(By.XPATH, xpath)
        if notifications:
            self.log.info('new version notification closed')
            notifications[0].click()
            

    def get_rscs(self):
        self.log.info('get rscs...')

        xpath = '//div[@location="id_2"]//div[@class="v-filterselect-button"]'
        try:
            self.wait_for('clickable', xpath, 40)
        except:
            pass    # agent without rsc is possible

        self._close_new_feature_notification()

        rsc_buttons = self.driver.find_elements(By.XPATH, xpath)

        if not rsc_buttons:
            return ['']     # agent has no rsc

        rsc_button = rsc_buttons[0]
        rsc_button.click()
        self.log.info('rsc_button clicked..1')

        rscs = list()

        for element in self._rsc_variants():
            span = element.find_element(By.XPATH, './/span')
            rscs.append(span.text)

        rsc_button.click()
        self.log.info(f'rsc_button clicked..2. rscs: {rscs}')

        return rscs

    def _rsc_variants(self):
        prev_page_xpath = '//div[@class="v-filterselect-prevpage"]/span[text()="Prev"]/..'
        next_page_xpath = '//div[@class="v-filterselect-nextpage"]/span[text()="Next"]/..'
        rsc_option_xpath = '//td[contains(@class, "gwt-MenuItem")]'

        # scroll backward
        while True:
            sleep(1)
            prev_elements = self.driver.find_elements(By.XPATH, prev_page_xpath)
            if prev_elements:
                prev_elements[0].click()
            else:
                break

        while True:
            sleep(1)
            # return options
            options = self.driver.find_elements(By.XPATH, rsc_option_xpath)
            for option in options:
                yield option

            # scroll forward
            next_elements = self.driver.find_elements(By.XPATH, next_page_xpath)
            if next_elements:
                next_elements[0].click()
            else:
                break

    def set_rsc(self, rsc):
        self.log.info(f'target rsc: "{rsc}"')
        if not rsc:
            return  # agent without rsc, setup must be skipped

        xpath = '//div[@location="id_2"]//div[@class="v-filterselect-button"]'
        self.wait_for('clickable', xpath, 60)

        rsc_b = self.driver.find_element(By.XPATH, xpath)
        while True:
            rsc_b.click()
            sleep(1.0)
            xpath = '//td[contains(@class, "gwt-MenuItem")]'
            elements = self.driver.find_elements(By.XPATH, xpath)
            if elements:
                break        
        for element in self._rsc_variants():
            span_elements = element.find_elements(By.XPATH, './/span')
            for span in span_elements:
                if span.text == rsc:
                    self.log.info('rsc found!')
                    element.click()
                    sleep(2)
                    return

        raise Exception(f"RSC '{rsc}' not found")

