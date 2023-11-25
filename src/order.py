from utils import LOG, get_periods
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

    def run(self, companies, periods):
        start_p, end_p = periods
        LOG.info(f'OrderHandler.run() target: {companies} ({start_p}-{end_p})')
        self.num_periods = get_periods(start_p=start_p, end_p=end_p)
        for company_name in companies:
            login, password = self.configuration.companies[company_name]
            company = Company(company=company_name, login=login, password=password)
            self.companies.append(company)

        for company in self.companies:
            company.get_reports(self.engine, self.num_periods)

