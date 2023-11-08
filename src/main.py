import PySimpleGUI as sg

from order import OrderHandler
from utils import LOG


def gui():
    layout = [[sg.Text("Manage Chrome")], [sg.Button("Start")]]

    # Create the window
    window = sg.Window("Emulator", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "Start":
            OrderHandler().run()
            break
        if event == sg.WIN_CLOSED:
            break

    window.close()


if __name__ == "__main__":

    LOG.info('\n\n\nGUI started..')
    gui()
    LOG.info('GUI stopped.')
