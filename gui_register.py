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
    layout = [[sg.Text('Nome')], # Entrada de nome do funcionario - Campo de visualização
              [sg.Input(key='-IN-')], # Entrada de nome do funcionario - Campo de Input
              [sg.Text('Camera', size=(40, 1), justification='center', font='Helvetica 20')], # Texto para a Camera
              [sg.Image(filename='', key='image')], # Local para a camera
              [sg.Button('Ligar Camera', size=(10, 1), font='Helvetica 14'), # Contém os campos de botões de acionamento
               sg.Button('Tirar Foto', size=(10, 1), font='Helvetica 14'),
               sg.Button('Parar', size=(10, 1), font='Any 14'),
               sg.Button('Sair', size=(10, 1), font='Helvetica 14')],
              [sg.Button('Cadastrar',size=(10, 1), font='Helvetica 14')],
               ]

    # Criação da janela
    window = sg.Window('Projeto e Engenharia de Software',
                       layout, location=(800, 400))
    
    cap = cv2.VideoCapture(0) # Identificando a Camera
    recording = False
    picture = False

    while True: # Loop principal de leitura dos valores.
        event, values = window.read(timeout=20)
        nome = values['-IN-']
        check_nome = bool(nome) # Verifica se o input de nome está vazio
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
            # img = np.full((480, 640), 255)
            # # this is faster, shorter and needs less includes
            # imgbytes = cv2.imencode('.png', img)[1].tobytes()
            # window['image'].update(data=imgbytes)

        elif recording: # Esta condição verifica se foi pressionado "Ligar a Camera" assim ela liga a leitura do OpenCV e projeta na tela
            ret, frame = cap.read()
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()
            window['image'].update(data=imgbytes)
            if picture and check_nome: # Aqui só irá começar caso tenha um nome no input e aperte para tirar a foto
                recording = False
                os.chdir('rostos') # Entrando no diretorio para gravação
                img_name = f"{nome}.png"
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                picture = False
                os.chdir('..') # Saindo do diretorio para permitir o restande do programa funcionar
            elif picture == True and check_nome == False: #Inicial o popup para indicar que para tirar a foto o nome do funcionario é obrigatorio
                sg.popup('Favor preencher o nome do funcionário antes de tirar a foto')
                picture = False

        elif event == "Cadastrar": # Inicia o mapeamento da imagem do rosto do funcionario
            try: 
                print(img_name)
                os.chdir('rostos') # Entrando no diretorio para leitura
                encodeTrain = treinamento(img_name)
                salvaEncode(encodeTrain, str(img_name.split(".")[0]))
                os.chdir('..') # Saindo do diretorio para permitir o restande do programa funcionar
            except IndexError: # Caso não o face_recognition não identificar um rosto ele vai retornar IndexError Out of Range, então nos preparamos para este erro
                os.chdir('..')
                sg.popup('Não foi possível cadastrar o rosto, favor tentar novamente')
                recording = True


main()






