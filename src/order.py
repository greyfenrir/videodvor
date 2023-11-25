from utils import LOG
from engine import Engine


class Company:
    def __init__(self, company, login, password):
        self.name = company
        self.login = login
        self.password = password

    def get_reports(self, engine, periods):
        engine.get_reports_for_periods(company=self, periods=periods)


class OrderHandler:
    def __init__(self, configuration):
        self.companies = list()
        self.num_periods = list()
        self.ordered_reports = dict()
        self.engine = Engine(ordered_reports=self.ordered_reports)
        self.configuration = configuration

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

    def run(self, companies, periods):
        start_p, end_p = periods
        LOG.info(f'OrderHandler.run() target: {companies} ({start_p}-{end_p})')
        self.num_periods = self.get_periods(start_p=start_p, end_p=end_p)
        for company_name in companies:
            login, password = self.configuration.companies[company_name]
            company = Company(company=company_name, login=login, password=password)
            self.companies.append(company)

        for company in self.companies:
            company.get_reports(self.engine, self.num_periods)

