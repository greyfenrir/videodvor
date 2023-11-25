import PySimpleGUI as sg

from order import OrderHandler
from utils import LOG, Configuration


def gui():
    def get_combo():
        names = list(configuration.companies.keys())
        lst = sg.Combo(names, default_value=names[0], font=('Arial Bold', 14),
                       expand_x=True, enable_events=True, readonly=False, key='combo')
        return lst

    periods = configuration.periods
    layout = [
        [sg.Text("Manage Chrome")],
        [get_combo()],
        [sg.Text("Start:"), sg.InputText(periods[0], key="start")],
        [sg.Text("End:"), sg.InputText(periods[1], key="end")],
        [sg.Button("Start")]]

    # Create the window
    window = sg.Window("Emulator", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "Start":
            company_name = values['combo']
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
