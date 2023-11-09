import PySimpleGUI as sg

from order import OrderHandler
from utils import LOG, configuration


def gui():
    def get_combo():
        names = list(configuration.companies.keys())
        lst = sg.Combo(names, default_value=names[0], font=('Arial Bold', 14),
                       expand_x=True, enable_events=True, readonly=False, key='combo')
        return lst

    layout = [[sg.Text("Manage Chrome")], [get_combo()], [sg.Button("Start")]]

    # Create the window
    window = sg.Window("Emulator", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "Start":
            OrderHandler().run(values['combo'])
            break
        if event == sg.WIN_CLOSED:
            break

    window.close()


if __name__ == "__main__":

    LOG.info('\n\n\nGUI started..')
    gui()
    LOG.info('GUI stopped.')
