import PySimpleGUI as sg
import datetime
from order import OrderHandler
from utils import LOG, Configuration, get_periods


def gui():
    def dd_companies():
        names = list(configuration.companies.keys()) + ['Все']
        lst = sg.Combo(names, default_value=names[0], font=('Arial Bold', 14),
                       expand_x=True, enable_events=True, readonly=False, key='d_company')
        return lst

    def dd_start():
        lst = sg.Combo(periods, default_value=periods[-1], font=('Arial Bold', 14),
                       expand_x=True, enable_events=True, readonly=False, key='d_start')
        return lst

    def dd_end():
        lst = sg.Combo(periods, default_value=periods[-1], font=('Arial Bold', 14),
                       expand_x=True, enable_events=True, readonly=False, key='d_end')
        return lst

    date = datetime.datetime.now()
    cur_year = int(date.strftime("%y"))
    cur_month = int(date.strftime("%m")) - 1
    if cur_month == 0:
        cur_month = 12
        cur_year -= 1
    cur_year += 2000
    num_periods = get_periods(f"{cur_month}.{cur_year-1}", f"{cur_month}.{cur_year}")[1:]
    periods = [f'{month:02d}.{year}' for month, year in num_periods]

    layout = [
        [sg.Text("Manage Chrome")],
        [dd_companies()],
        [sg.Text("Start:"), dd_start()],
        [sg.Text("End:"), dd_end()],
        [sg.Button("Start")]]

    # Create the window
    window = sg.Window("Emulator", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "Start":
            if periods.index(values['d_start']) > periods.index(values['d_end']):
                sg.popup_error(f'Неверный порядок периодов')
                continue

            company_name = values['d_company']
            if company_name in configuration.companies.keys():
                companies = [company_name]
            else:
                companies = configuration.companies.keys()
            p_start, p_end = values['start'], values['end']
            OrderHandler(configuration=configuration).run(companies=companies, periods=(p_start, p_end))
            break
        if event == sg.WIN_CLOSED:
            break

    window.close()


if __name__ == "__main__":
    configuration = Configuration()
    LOG.info('\n\n\nGUI started..')
    gui()
    LOG.info('GUI stopped.')
