import os.path

from utils import configuration
from engine import Engine


class Company:
    def __init__(self, company, login, password):
        self.name = company
        self.login = login
        self.password = password

    def get_reports(self, engine, periods):
        engine.get_reports_for_periods(company=self, periods=periods)


class Order:
    def __init__(self):
        self.periods = None
        self.companies = list()


class OrderHandler:
    def __init__(self):
        self.companies = list()
        start_period = '03.2023'
        end_period = '05.2023'
        self.num_periods = self.get_periods(start_p=start_period, end_p=end_period)
        self.ordered_reports = dict()
        self.engine = Engine(ordered_reports=self.ordered_reports)

    @staticmethod
    def get_periods(start_p, end_p):
        periods = []
        first_m, first_y = [int(part) for part in start_p.split('.')]
        last_m, last_y = [int(part) for part in end_p.split('.')]
        periods.append((first_m, first_y))
        while not (first_m == last_m and first_y == last_y):
            first_m += 1
            if first_m > 12:
                first_m = 1
                first_y += 1

            periods.append((first_m, first_y))
        return periods

    def run(self, company_name):
        login, password = configuration[company_name]
        company = Company(company=company_name, login=login, password=password)
        self.companies.append(company)
        for company in self.companies:
            company.get_reports(self.engine, self.num_periods)

        for company in self.companies:
            company.get_reports(self.engine, self.ordered_reports)
