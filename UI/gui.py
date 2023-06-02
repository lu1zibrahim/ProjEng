import PySimpleGUI as sg      

sg.theme('Black')    # General Theme

right_menu_layout = [[sg.Button('Acessar Camera')],
          [sg.Button('Acessar Logs')],
          [sg.Button('Lista de Usuários')],
          [sg.Button('Cadastrar Novo Usuário')],
          ]      

layout = [
    [sg.Column(right_menu_layout, element_justification='right', expand_x = True)]
]
window = sg.Window('Main Page', layout, size=(1280,720))      

while True:                             # The Event Loop
    event, values = window.read() 
    print(event, values)       
    if event == sg.WIN_CLOSED or event == 'Exit':
        break      

window.close()