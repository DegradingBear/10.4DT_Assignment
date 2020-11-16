import PySimpleGUI as gui

init = 1

layout = []

def declareLayout(init):
    global layout
    layout = [
        [gui.Text("Hello World", key=init)],
        [gui.Button("reload", key=f'reload{init}')]
    ]

declareLayout(1)
window = gui.Window("hi", layout)

while True:
    event, values = window.read()

    if event == gui.WIN_CLOSED:
        break
    if event == f'reload{init}':
        gui.popup_ok("closing window")
        window.close()
        init += 1
        declareLayout(init)
        gui.theme("DarkAmber")
        window = gui.Window("hi", layout)
