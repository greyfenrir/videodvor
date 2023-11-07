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

    def configure(self):
        # todo: read it from config file instead
        companies = read_config()
        company = 'НВА'
        login, password = companies[company]
        self.companies.append(Company(company=company, login=login, password=password))
        start_period = '03.2023'
        end_period = '05.2023'
        self._set_periods(start_p=start_period, end_p=end_period)

    def _set_periods(self, start_p, end_p):
        self.periods = []
        first_m, first_y = [int(part) for part in start_p.split('.')]
        last_m, last_y = [int(part) for part in end_p.split('.')]
        self.periods.append((first_m, first_y))
        while not (first_m == last_m and first_y == last_y):
            first_m += 1
            if first_m > 12:
                first_m = 1
                first_y += 1

            self.periods.append((first_m, first_y))


class OrderHandler:
    def __init__(self):
        self.order = Order()
        self.order.configure()
        self.ordered_reports = dict()
        self.engine = Engine(ordered_reports=self.ordered_reports)

    def run(self):
        for company in self.order.companies:
            company.get_reports(self.engine, self.order.periods)


def read_config():
    with open('config.cfg', mode='r', encoding='utf-8') as _f:
        companies = _f.read()

    return eval(companies)
