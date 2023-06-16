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

camera = cv2.VideoCapture(0)
rodando = False
detection = 'not_found'
faces = []

fontScale = 1
color = (0, 255, 0)
thickness = 2
font = cv2.FONT_HERSHEY_SIMPLEX
faces = []
nomes = []
distancias = []

pasta = 'rostos/'

#img = f'rostos/{nome}.jpg' #insira o nome do arquvio, e deixe ele na mesma pasta desse .py

def procuraRosto(frame):
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces_detect = face_cascade.detectMultiScale(gray, 1.3, 4)
        if np.shape(faces_detect)[0] > 0:
            detection = 'found'
        else:
            detection = 'not_found'
    except:
        detection = 'not_found'
        pass
    
    return faces_detect, detection
    
    
def cortaRosto(faces_detect, frame):
    for (x, y, w, h) in faces_detect: 
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2) 
        rosto_img = frame[y:y + h, x:x + w]
        loc_x = x
        loc_y = y
        loc_w = w
        loc_h = h
    return rosto_img, loc_x, loc_y, loc_w, loc_h
    
for diretorio, subpastas, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        nome = os.path.splitext(arquivo)[0]
        extensao = os.path.splitext(arquivo)[1]
        arquivo = os.path.join(pasta,arquivo)
        
        if (extensao == ".txt"):
            aux_load = np.loadtxt(arquivo)
            faces.append(aux_load)
            nomes.append(nome)

qtd_pessoas = np.shape(nomes)[0]

registros_entrada = []
registros_saida = []
nomes_entrada = []

def main():

    sg.theme('Black')

    # define the window layout
    layout = [[sg.Text('Camera', size=(40, 1), justification='center', font='Helvetica 20')], # Texto para a Camera
              [sg.Image(filename='', key='image')], # Local para a camera
              [sg.Button('Ligar Camera', size=(10, 1), font='Helvetica 14'), # Contém os campos de botões de acionamento
               sg.Button('Tirar Foto', size=(10, 1), font='Helvetica 14')],
              [sg.Button('Verificar',size=(10, 1), font='Helvetica 14')],
               ]

    # Criação da janela
    window = sg.Window('Projeto e Engenharia de Software',
                       layout, location=(800, 400))
    
    cap = cv2.VideoCapture(0) # Identificando a Camera
    recording = False
    picture = False
    verificando = False

    while True: # Loop principal de leitura dos valores.
        event, values = window.read(timeout=20)
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
        
        elif event == "Verificar": # Inicia o mapeamento da imagem do rosto do funcionario
            recording = False
            verificando = True

        elif recording: # Esta condição verifica se foi pressionado "Ligar a Camera" assim ela liga a leitura do OpenCV e projeta na tela
            ret, frame = cap.read()
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()
            window['image'].update(data=imgbytes)
            # if picture: # Aqui só irá começar caso tenha um nome no input e aperte para tirar a foto
            #     recording = False
            #     os.chdir('rostos') # Entrando no diretorio para gravação
            #     img_name = f"{nome}.png"
            #     cv2.imwrite(img_name, frame)
            #     print("{} written!".format(img_name))
            #     picture = False
            #     os.chdir('..') # Saindo do diretorio para permitir o restande do programa funcionar

        elif verificando: # Inicia o mapeamento da imagem do rosto do funcionario
            aux_compare = 0
            status, frame = camera.read()
            frame = cv2.resize(frame, (640,480), interpolation = cv2.INTER_AREA)
            window['image'].update(data=cv2.imencode('.ppm', camera.read()[1])[1].tobytes())
            aux_detect = 0
            


            while aux_detect < 5:
                faces_detect, detection = procuraRosto(frame)
                if detection == "found":
                    rosto, loc_x, loc_y, loc_w, loc_h = cortaRosto(faces_detect, frame)
                    rosto_test = cv2.cvtColor(rosto,cv2.COLOR_BGR2RGB)
                    
                    if np.shape(fr.face_encodings(rosto_test))[0]==0:
                        print('USUÁRIO DESCONHECIDO - ACESSO NEGADO')
                        pass
                    else:
                        encodeTest = fr.face_encodings(rosto_test)[0]
                        
                        while aux_compare < (qtd_pessoas):
                            encodeTrain = faces[aux_compare]
                            comparacao = fr.compare_faces([encodeTrain],encodeTest,tolerance=0.48) #Comparação Face Atual X Face Treinada.
                            distancia = fr.face_distance([encodeTrain],encodeTest)
                            #print(comparacao,distancia)
                        
                            if comparacao == [True]:
                                nome = nomes[aux_compare]
                                try: 
                                    detect = frame
                                    cv2.rectangle(detect, (loc_x, loc_y), (loc_x+loc_w, loc_y+loc_h) ,(0,255,0),2)
                                    org = (loc_x, loc_y)
                                    cv2.putText(detect, nome, org , font, fontScale, color, thickness, cv2.LINE_AA, False)

                                    if len(registros_entrada) == 0:
                                        """
                                        Primeiramente conferir se a lista estiver vazia, caso esteja, irá inserir o primeiro usuário
                                        """
                                        agora = datetime.now()
                                        registros_entrada.append([nome,agora])
                                        print(registros_entrada)
                                    else:    
                                        for registro in registros_entrada:
                                            """
                                            Esse loop funciona para percorrer a listagem de registros se o funcionário estiver já registrado a entrada, ele vai registrar a saída e apagar da lista de funcionários que estão no local.
                                            """
                                            if nome in registro[0]:
                                                saida = datetime.now()
                                                tempo_permanencia = saida - registro[1]
                                                print("SAIDA REGISTRADA: "+nome+" - TEMPO DE PERMANENCIA: "+str(tempo_permanencia))
                                                registros_saida.append([nome, registro[1], saida,tempo_permanencia])
                                                index_nome = registros_entrada[0].index(nome)
                                                registros_entrada.pop(index_nome)
                                                print(registros_entrada)
                                                print(registros_saida)
                                            else:
                                                agora = datetime.now()
                                                registros_entrada.append([nome,agora])

                                    print("ACESSO LIBERADO: "+str(nome))
                                    verificando = False
                                    recording = True
                                    sg.popup(f'Usuario Liberado, Bem Vindo(a) - {nome}')

                                    # print(registros_entrada)
                                    # print(nomes_entrada)
                                    sleep(2)
                                    
                                    break
                                except:
                                    print('erro ao inserir credenciais...')
                                    comparacao = False
                                    pass
                            else:
                                aux_compare += 1
                    break

                aux_detect += 1 
                if aux_detect == 5 :
                    print("NÃO FOI POSSIVEL IDENTIFICAR")   

main()






