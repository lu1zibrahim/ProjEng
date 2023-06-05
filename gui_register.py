import PySimpleGUI as sg      
import cv2
import numpy as np
import face_recognition as fr
from datetime import datetime
import os
from time import sleep

# sg.theme('Black')    # General Theme

# right_menu_layout = [[sg.Button('Acessar Camera')],
#           [sg.Button('Acessar Logs')],
#           [sg.Button('Lista de Usuários')],
#           [sg.Button('Cadastrar Novo Usuário')],
#           ]      

# layout = [
#     [sg.Column(right_menu_layout, element_justification='right', expand_x = True)]
# ]
# window = sg.Window('Main Page', layout, size=(1280,720))      

# while True:                             # The Event Loop
#     event, values = window.read() 
#     print(event, values)       
#     if event == sg.WIN_CLOSED or event == 'Exit':
#         break      

# window.close()

faces = []

#img = f'rostos/{nome}.jpg' #insira o nome do arquvio, e deixe ele na mesma pasta desse .py

def treinamento(local_img):
    img_to_train = fr.load_image_file(local_img)
    img_to_train = cv2.cvtColor(img_to_train,cv2.COLOR_BGR2RGB)
    faceLoc = fr.face_locations(img_to_train)[0]
    cv2.rectangle(img_to_train,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(0,255,0),2)
    encodeTrain = fr.face_encodings(img_to_train)[0]
    
    return encodeTrain

def salvaEncode(encodeTrain, nome):
    nome_txt = nome+".txt"
    np.savetxt(nome_txt, encodeTrain)
    


def main():

    sg.theme('Black')

    # define the window layout
    layout = [[sg.Text('Nome')],
              [sg.Input(key='-IN-')],
              [sg.Text('Camera', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image')],
              [sg.Button('Ligar Camera', size=(10, 1), font='Helvetica 14'),
               sg.Button('Tirar Foto', size=(10, 1), font='Helvetica 14'),
               sg.Button('Parar', size=(10, 1), font='Any 14'),
               sg.Button('Sair', size=(10, 1), font='Helvetica 14')],
              [sg.Button('Cadastrar',size=(10, 1), font='Helvetica 14')],
               ]

    # create the window and show it without the plot
    window = sg.Window('Demo Application - OpenCV Integration',
                       layout, location=(800, 400))
    
    cap = cv2.VideoCapture(0)
    recording = False
    picture = False

    while True:
        event, values = window.read(timeout=20)
        nome = values['-IN-']
        check_nome = bool(nome)
        if event == 'Sair' or event == sg.WIN_CLOSED:
            return

        elif event == 'Ligar Camera':
            recording = True
            picture = False

        elif event == 'Tirar Foto':
            picture = True

        elif event == 'Parar':
            recording = False
            picture = False
            print(nome)
            print(check_nome)
            # img = np.full((480, 640), 255)
            # # this is faster, shorter and needs less includes
            # imgbytes = cv2.imencode('.png', img)[1].tobytes()
            # window['image'].update(data=imgbytes)

        elif recording:
            ret, frame = cap.read()
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()
            window['image'].update(data=imgbytes)
            if picture and check_nome:
                recording = False
                os.chdir('rostos')
                img_name = f"{nome}.png"
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                picture = False
                os.chdir('..')
            elif picture == True and check_nome == False:
                sg.popup('Favor preencher o nome do funcionário antes de tirar a foto')
                picture = False

        elif event == "Cadastrar":
            print(img_name)
            os.chdir('rostos')
            encodeTrain = treinamento(img_name)
            salvaEncode(encodeTrain, str(img_name.split(".")[0]))
            os.chdir('..')


main()






