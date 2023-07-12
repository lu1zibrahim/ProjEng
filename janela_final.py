import PySimpleGUI as sg      
import cv2
import numpy as np
import pandas as pd
import face_recognition as fr
import os
import csv
import operator
from time import sleep
from datetime import datetime
from datetime import timedelta

sg.theme('Black')   
faces = []
detection = 'not_found'
faces = []
fontScale = 1
color = (0, 255, 0)
thickness = 2
font = cv2.FONT_HERSHEY_SIMPLEX
faces = []
nomes = []
registro_array=[]
distancias = []
pasta = 'rostos/'
aux_exit = 0
thresh_value = 0.48
senha_adm = str(1234)
aux_camera = 0
time_limit_minute = 1
time_limit_seconds = int(time_limit_minute)*60
camera = cv2.VideoCapture(aux_camera)


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

def sort_table(table, cols, descending=False):
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col), reverse=descending)
        except Exception as e:
            sg.popup_error('Error in sort_table', 'Exception in sort_table', e)
    return table


def read_csv_file(filename):
    data = []
    header_list = []
    if filename is not None:
        try:
            with open(filename, encoding='UTF-16') as infile:
                reader = csv.reader(infile,delimiter='\t')
                # reader = fix_nulls(filename)
                header_list = next(reader)
                try:
                    data = list(reader)  # read everything else into a list of rows
                except Exception as e:
                    print(e)
                    sg.popup_error('Error reading file', e)
                    return None, None
        except:
            with open(filename,  encoding='utf-8') as infile:
                reader = csv.reader(infile, delimiter=',')
                # reader = fix_nulls(filename)
                header_list = next(reader)
                try:
                    data = list(reader)  # read everything else into a list of rows
                except Exception as e:
                    with open(filename) as infile:
                        reader = csv.reader(infile, delimiter=',')
                        # reader = fix_nulls(filename)
                        header_list = next(reader)
                        try:
                            data = list(reader)  # read everything else into a list of rows
                        except Exception as e:
                            print(e)
                            sg.popup_error('Error reading file', e)
                            return None, None
    return data, header_list

def make_window1():
    sg.theme('Black')
    layout = [[sg.Column([
            [sg.Image('UI/images/unifesp.png')],
              [sg.Text('                    '),sg.Button("", image_filename='UI/Icons/acessar_camera.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Janela_verificar"),
              sg.Button("", image_filename='UI/Icons/cadastrar_usuario.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Janela_cadastrar"),
              sg.Button("", image_filename='UI/Icons/acessar_logs_2.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Janela_log")],
              ], justification='center')],
              [sg.Text('                                                         '),sg.Button("", image_filename='UI/Icons/monitorando.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Monitoramento"),sg.Button("", image_filename='UI/Icons/configuracao.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="config")]
              ]

    return sg.Window('Home', layout,resizable=True,  finalize=True)


def make_window2():
    sg.theme('Black')
    layout = [[sg.Column([
        [sg.Text('Camera', size=(40, 1), justification='center', font='Helvetica 20')], # Texto para a Camera
              [sg.Text('                        '),sg.Image(filename='', key='image')], # Local para a camera
              [sg.Button("", image_filename='UI/Icons/ligar_camera_final.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Ligar Camera"),
               sg.Button("", image_filename='UI/Icons/verificar_final.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Verificar"),sg.Button("", image_filename='UI/Icons/PaginaInicial.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Home")],
                 ], justification='center')]
               ]
    

    return sg.Window('Janela Verificar', layout,resizable=True, finalize=True)


def make_window3():
    sg.theme('Black')
    layout = [[sg.Column([
            [sg.Text('Nome do Colaborador:    '), sg.Input(key='-IN-', size=(40,2), justification='center', font='Helvetica 15')],
            [sg.Text('Registro do Colaborador: '), sg.Input(key='re_input', size=(5,2), justification='center', font='Helvetica 15')], 
              [sg.Image(filename='', key='image')],# Local para a camera
              [sg.Button("", image_filename='UI/Icons/ligar_camera_final.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Ligar Camera"), # Contém os campos de botões de acionamento
               sg.Button("", image_filename='UI/Icons/tirar_foto_final.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Tirar Foto"), 
               sg.Button("", image_filename='UI/Icons/cadastrar_final.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Cadastrar")],
              [sg.Text('                                            '),sg.Button("", image_filename='UI/Icons/PaginaInicial.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Home")],
    ], justification='center')],
        [sg.Text('               Carregar foto: '), sg.Input("", key="image_load",size=(65,1)),sg.FilesBrowse(size=(7,1))]
               ]
    return sg.Window('Janela Cadastrar', layout, resizable=True, finalize=True)
    # Criação da janela


def make_window4():
    sg.theme('Black')

    original_database, header_list = read_csv_file('registro_saida.csv')
    data = original_database
    layout = [  [sg.Text(f'{len(data)} Registro(s) na tabela', font='_ 18')],
                [sg.Text('Filtros:')],
                [sg.Combo(['Nome', 'Registro'],default_value='Registro',key="type_filter"),sg.Input('',size=(20,2),key='filter_input'),sg.Button ('Aplicar',key='go_filter'), sg.Button ('Limpar filtros',key='clear')],
                [sg.Text(k='-RECORDS SHOWN-', font='_ 18')],
                [sg.Text(k='-SELECTED-')],
          
                [sg.Table(values=data, headings=header_list, max_col_width=25,
                        auto_size_columns=True, display_row_numbers=True, vertical_scroll_only=True,
                        justification='right', num_rows=10,
                        key='-TABLE-', selected_row_colors='red on yellow', enable_events=True,
                        expand_x=True, expand_y=True,
                        enable_click_events=True)],
                [sg.Sizegrip()],
                [sg.Button("", image_filename='UI/Icons/PaginaInicial.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Home")]]
    return sg.Window('Janela de Logs', layout,layout, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT,  resizable=True, finalize=True), data, header_list

def make_window5():
    sg.theme('Black')
    layout = [
            [sg.Image('UI/images/unifesp.png')],
            [sg.Text('Selecione o parâmetro de tolerancia da identificação visual:'), sg.Combo([0.46,0.47,0.48,0.49,0.50],default_value=thresh_value,key='threshold')],
            [sg.Text('Selecione o dispositivo de vídeo:'), sg.Combo(["Principal",'Secundario'],default_value="Principal",key='camera_choose')],
            [sg.Text('Determine o tempo de  permanencia máximo para o indicativo de alerta:'),sg.Input(time_limit_minute, key='input_limit',size=(10,2)),sg.Text(' Minutos')],
            [sg.Button ('Aplicar',key='go_config')]
            ]
    return sg.Window('Janela Configuracoes', layout, resizable=True, finalize=True)

def make_window6():
    sg.theme('Black')
    headings = ['Nome', 'Registro', 'Entrada','Maximo','Situacao']
    layout = [[sg.Table(values = registros_entrada, headings = headings,
                       auto_size_columns = True,
                       display_row_numbers = False,
                       justification = 'Center',
                       key = '-TABLE-',
                       enable_events = False,
                       expand_x = True,
                       expand_y = True
                       )],
              [sg.Button("", image_filename='UI/Icons/PaginaInicial.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Home"),sg.Button("", image_filename='UI/Icons/monitorando.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Atualizar")]]
            
    return sg.Window('Janela Monitoramento', layout, size=(800,800), resizable=True, finalize=True)
 
### COMEÇA O PROGRAMA:
    
window1, window2, window3, window4, window5, window6 = make_window1(), None, None, None, None, None
window1.move(300,10)
aux_exit = 0

for diretorio, subpastas, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        nome = ((os.path.splitext(arquivo)[0]).split('---'))[0]
        registro = ((os.path.splitext(arquivo)[0]).split('---'))[1]
        extensao = os.path.splitext(arquivo)[1]
        arquivo = os.path.join(pasta,arquivo)
        
        if (extensao == ".txt"):
            aux_load = np.loadtxt(arquivo)
            faces.append(aux_load)
            nomes.append(nome)
            registro_array.append(registro)
qtd_pessoas = np.shape(nomes)[0]

if os.path.exists('registro_saida.csv'):
    inicio_saida = pd.read_csv('registro_saida.csv')
    registros_saida = inicio_saida.values.tolist()
    #print(registros_saida)
else:
    #print('not')
    registros_saida = []

registros_entrada = []
nomes_entrada = []
recording = False
verificando = False
black_mask = cv2.imread('UI/images/black_mask.png')

while True:
    window, event, values = sg.read_all_windows()
    if window == window1 and event in (sg.WIN_CLOSED, 'Exit'):
        break
    
    if window == window1 and event == 'Monitoramento':
        window1.hide()
        window6 = make_window6()
    
    if window == window1 and event == 'config':
        password = sg.popup_get_text('ACESSO RESTRITO AO ADMINISTRADOR!\nProcure a equipe responsável ou digite a senha de acesso: ',password_char='*')
        if password == senha_adm:
            passport = 'ok'
            window1.hide()
            window5 = make_window5()
            
        else:
            sg.popup("Senha Incorreta! Tente novamente.")

    if window == window1:
        if event == 'Janela_verificar':
            window1.hide()
            window2 = make_window2()
            imgbytes = cv2.imencode('.png', black_mask)[1].tobytes()
            window2['image'].update(data=imgbytes)
            recording = True
            verificando = False
            window2.move(300,100)
            
        elif event == 'Janela_cadastrar':
            window1.hide()
            window3 = make_window3()
            imgbytes = cv2.imencode('.png', black_mask)[1].tobytes()
            window3['image'].update(data=imgbytes)
            window3.move(300,100)
            recording = True
            picture = False
            
        elif event == 'Janela_log':
            window1.hide()
            window4, data, header_list = make_window4()
            window4.move(300,10)

    if window == window2:
        recording = True
        verificando = False

        while True:
            event, values = window.read(timeout=20)
            if event == 'Sair' or event == sg.WIN_CLOSED:
                reg_saida = pd.DataFrame(registros_saida, columns =['Nome','Registro', 'Entrada', 'Saida','Duracao'])
                reg_saida.to_csv('registro_saida.csv', index=False)
                aux_exit = 1
                break

            elif event == 'Ligar Camera':
                verificando = False
                recording = True

            elif event == 'Home':
                reg_saida = pd.DataFrame(registros_saida, columns =['Nome','Registro', 'Entrada', 'Saida','Duracao'])
                reg_saida.to_csv('registro_saida.csv', index=False)
                window2.close()
                window1.un_hide()
                break

            elif event == 'Parar':
                recording = False
                verificando = False
                
            
            elif event == "Verificar": 
                recording = False
                verificando = True

            elif recording: 
                ret, frame = camera.read()
                imgbytes = cv2.imencode('.png', frame)[1].tobytes()
                window['image'].update(data=imgbytes)
                

            elif verificando: 
                aux_compare = 0
                status, frame = camera.read()
                frame = cv2.resize(frame, (640,480), interpolation = cv2.INTER_AREA)
                window['image'].update(data=cv2.imencode('.ppm', camera.read()[1])[1].tobytes())
                aux_detect = 0
                


                while aux_detect < 5:
                    faces_detect, detection = procuraRosto(frame)
                    if detection == "found":
                        detection == ""
                        rosto, loc_x, loc_y, loc_w, loc_h = cortaRosto(faces_detect, frame)
                        rosto_test = cv2.cvtColor(rosto,cv2.COLOR_BGR2RGB)
                        
                        if np.shape(fr.face_encodings(rosto_test))[0]==0:
                            print('USUÁRIO DESCONHECIDO - ACESSO NEGADO')
                            pass
                        else:
                            encodeTest = fr.face_encodings(rosto_test)[0]
                            
                            while aux_compare < (qtd_pessoas):
                                encodeTrain = faces[aux_compare]
                                comparacao = fr.compare_faces([encodeTrain],encodeTest,tolerance=thresh_value) #Comparação Face Atual X Face Treinada.
                                distancia = fr.face_distance([encodeTrain],encodeTest)
                            
                                if comparacao == [True]:
                                    nome = nomes[aux_compare]
                                    re = registro_array[aux_compare]

                                    try: 
                                        detect = frame
                                        cv2.rectangle(detect, (loc_x, loc_y), (loc_x+loc_w, loc_y+loc_h) ,(0,255,0),2)
                                        org = (loc_x, loc_y)
                                        cv2.putText(detect, nome, org , font, fontScale, color, thickness, cv2.LINE_AA, False)
                            
                                        if nome in registros_entrada:
                                            aux_saida = 1
                                        else:
                                            aux_saida = 0
                                            
                                        if len(registros_entrada) == 0:
                                            agora = datetime.now()
                                            maximo = agora + timedelta(seconds=time_limit_seconds)
                                            situacao = 'Normal'
                                            registros_entrada.append([nome,re,agora,maximo,situacao])
                                    
                                        else:
                                            if nome in registros_entrada:
                                                for registro in registros_entrada:
                                                    if nome in registro[0]:
                                                        saida = datetime.now()
                                                        tempo_permanencia = saida - registro[2]
                                                        print("SAIDA REGISTRADA: "+nome+" - TEMPO DE PERMANENCIA: "+str(tempo_permanencia))
                                                        registros_saida.append([nome, registro[1], registro[2], saida ,tempo_permanencia])
                                                        index_nome = registros_entrada[0].index(nome)
                                                        registros_entrada.pop(index_nome)
                                                        aux_saida = 1
                                                    else:
                                                        agora = datetime.now()
                                                        registros_entrada.append([nome, re ,agora,maximo,situacao])
   
                                            else:
                                                agora = datetime.now()
                                                maximo = agora + timedelta(seconds=time_limit_seconds)
                                                situacao = 'Normal'
                                                registros_entrada.append([nome,re,agora,maximo,situacao])
                                                
                                                
                                        print("ACESSO LIBERADO: "+str(nome))
                                        verificando = False
                                        recording = True
                                        
                                        if aux_saida==1:
                                            sg.popup(f'Saida Autorizada. Muito obrigado {nome}')
                                        else:
                                            sg.popup(f'Entrada Autorizada. Atente-se ao tempo máximo de permanencia neste local. Seja bem Vindo(a) {nome}')
                                            
                                        comparacao = False
                                        break
                                    except:
                                        print('erro ao inserir credenciais...')
                                        comparacao = False
                                        aux_compare += 1
                                        pass
                                else:
                                    aux_compare += 1
                        
                        break

                    aux_detect += 1 
                    if aux_detect == 5 :
                        print("NÃO FOI POSSIVEL IDENTIFICAR")
                        verificando = False
                        recording = True
                        
    
    
    if window == window3:
            recording = False
            picture = False
            while True:
                event, values = window.read(timeout=20)
                if event == 'Sair' or event == sg.WIN_CLOSED:
                    aux_exit = 1
                    break

                elif event == 'Ligar Camera':
                    recording = True
                    picture = False

                elif event == 'Tirar Foto':
                    picture = True
                    # os.chdir('rostos')
                    # img_name = str(nome)+"---"+str(re)+".png"
                    # cv2.imwrite(img_name, frame)
                    # print("{} written!".format(img_name))
                    # image_file_temp = cv2.imread(img_name)
                    # os.chdir('..') # Saindo do diretorio para permitir o restande do programa funcionar

                elif event == 'Parar':
                    recording = False
                    picture = False

                elif event == 'Home':
                    window3.close()
                    window1.un_hide()
                    break
                    
                                 

                elif recording: 
                    ret, frame = camera.read()
                    imgbytes = cv2.imencode('.png', frame)[1].tobytes()
                    window['image'].update(data=imgbytes)
                    nome = values['-IN-']
                    re = values['re_input']
                    check_nome = bool(nome) 
                    if picture and check_nome: # Aqui só irá começar caso tenha um nome no input e aperte para tirar a foto
                        recording = False
                        os.chdir('rostos') # Entrando no diretorio para gravação
                        img_name = str(nome)+"---"+str(re)+".png"
                        cv2.imwrite(img_name, frame)
                        print("{} written!".format(img_name))
                        picture = False
                        os.chdir('..') # Saindo do diretorio para permitir o restande do programa funcionar
                    elif picture == True and check_nome == False: #Inicial o popup para indicar que para tirar a foto o nome do funcionario é obrigatorio
                        sg.popup('Favor preencher o nome do funcionário antes de tirar a foto')
                        picture = False

                  

                if event == "Cadastrar": # Inicia o mapeamento da imagem do rosto do funcionario
                    image_adress = values['image_load']
                    if image_adress != '':
                        image_file_temp = image_adress
                        img_file = cv2.imread(image_adress)
                        nome = values['-IN-']
                        re = values['re_input']
                        img_name = str(nome)+"---"+str(re)+".png"
                        os.chdir('rostos') # Entrando no diretorio para gravação
                        img_name = str(nome)+"---"+str(re)+".png"
                        cv2.imwrite(img_name, img_file)

                        os.chdir('..') # Saindo do diretorio para permitir o restande do programa funcionar
                    else:
                        image_file_temp = img_name
                    try: 
                        #print('aqui2')
                        os.chdir('rostos')
                        encodeTrain = treinamento(image_file_temp)
                        try:
                            salvaEncode(encodeTrain, str(img_name.split(".")[0]))
                            os.chdir('..')
                        except:
                            os.chdir('..')
                        
                        
                        #CAREGGA OS REGISTROS
                        for diretorio, subpastas, arquivos in os.walk(pasta):
                            for arquivo in arquivos:
                                nome = (os.path.splitext(arquivo)[0]).split('---')[0]
                                re = (os.path.splitext(arquivo)[0]).split('---')[1]
                                extensao = os.path.splitext(arquivo)[1]
                                arquivo = os.path.join(pasta,arquivo)
                                
                                if (extensao == ".txt"):
                                    aux_load = np.loadtxt(arquivo)
                                    faces.append(aux_load)
                                    nomes.append(nome)
                                    registro_array.append(re)
    
                        qtd_pessoas = np.shape(nomes)[0]
                        sg.popup('Face cadastrada com sucesso!')
                    except IndexError: # Caso não o face_recognition não identificar um rosto ele vai retornar IndexError Out of Range, então nos preparamos para este erro
                        sg.popup('Não foi possível cadastrar o rosto, favor tentar novamente')
                        picture = False
                        recording = True

    if window == window4:
        window.bind("<Control_L><End>", '-CONTROL END-')
        window.bind("<End>", '-CONTROL END-')
        window.bind("<Control_L><Home>", '-CONTROL HOME-')
        window.bind("<Home>", '-CONTROL HOME-')
        #original_data = data        # save a copy of the data
        csv.field_size_limit(2147483647)        # enables huge tables

        while True:
            event, values = window.read()
            # print(event, values)
            if event in (sg.WIN_CLOSED, 'Sair'):
                aux_exit = 1
                break
            if values['-TABLE-']:           # Show how many rows are slected
                window['-SELECTED-'].update(f'{len(values["-TABLE-"])} rows selected')
            else:
                window['-SELECTED-'].update('')

            if event == 'Home':
                window4.close()
                window1.un_hide()
                break
            
            if event == "go_filter":
                tipo_filtro = values['type_filter']
                chave_filtro = values['filter_input']
                dataframe = pd.DataFrame(data, columns =header_list)
                
                if tipo_filtro == "Nome":
                    indexNames = dataframe[dataframe['Nome'] != chave_filtro].index
                    filter_data = dataframe.drop(indexNames)
                    filter_data.reset_index(inplace=True, drop=True)
                    filter_list = filter_data.values.tolist()
                    window4['-TABLE-'].update(values = filter_list)
                    
                elif tipo_filtro == "Registro":
                    indexNames = dataframe[dataframe['Registro'] != chave_filtro].index
                    filter_data = dataframe.drop(indexNames)
                    filter_data.reset_index(inplace=True, drop=True)
                    filter_list = filter_data.values.tolist()
                    window4['-TABLE-'].update(values = filter_list)
                    
            if event == "clear":
                window4['-TABLE-'].update(values = data)
                    
                
            
    if window == window5 and event == 'go_config':
        thresh_value = values['threshold']
        time_limit_minute = values['input_limit']
        time_limit_minute = int(time_limit_minute)
        
        if values['camera_choose'] == 'Principal':
            if aux_camera != 0:
                aux_camera = 0

                camera = cv2.VideoCapture(aux_camera)
                ret, frame = camera.read()
                if np.shape(frame) == ():
                    sg.popup("Dispositivo não encontrado.")
                        
            else:
                aux_camera = 0
        else:
            if aux_camera != 1:
                aux_camera = 1
                camera = cv2.VideoCapture(aux_camera)
                ret, frame = camera.read()
                np.shape(frame) == ()
                if np.shape(frame) == ():
                    sg.popup("Dispositivo não encontrado.")
            else:
                aux_camera = 1
                
        window5.hide()
        window1.un_hide()
    


    if window == window5 and event in (sg.WIN_CLOSED, 'Exit'):
        break
            
    if aux_exit == 1:
        break
    
    if window == window6:
        time_limit_seconds = time_limit_minute * 60
        tempo_maximo = timedelta(seconds=time_limit_seconds)
        reg_entrada = pd.DataFrame(registros_entrada, columns = ['Nome','Registro','Entrada','Maximo','Situacao'])
        reg_entrada[['Entrada', 'Maximo']].apply(pd.to_datetime)
        while True:
            event, values = window.read(timeout=20) 
            monitorando = False
            if event == "Atualizar" and len(registros_entrada) != 0:
                sg.popup('Monitoramento em curso.')
                monitorando = True
            elif event =="Atualizar" and len(registros_entrada) == 0:
                sg.popup('Não há colaboradores ativos.')
                monitorando = False
            while monitorando:
                reg_entrada['Compare'] = datetime.now() > reg_entrada['Maximo']
                comparacao = dict(zip(reg_entrada.Nome, reg_entrada.Compare))
                passou_horario = [i for i in comparacao.values()]
              
                if True in passou_horario:
                    reg_entrada.loc[reg_entrada['Compare'] == True, 'Situacao'] = 'Excedente' 
                    new_reg = reg_entrada.loc[(reg_entrada['Compare'] == True), ['Nome','Registro','Entrada','Maximo','Situacao']]
                    registros_entrada = new_reg.values.tolist()
                    window6['-TABLE-'].update(values = registros_entrada)
                    pop_up = sg.popup_yes_no('Existem funcionários acima do tempo máximo de permanencia, deseja ver a lista dos colaborados com tempo excedênte?')
                    if pop_up == 'Yes':
                        monitorando = False 
                    elif pop_up == 'No':
                        sleep(5)
                else:
                    sleep(5)
           
            if event == sg.WIN_CLOSED:
                aux_exit = 1
                break
            
            if event == 'Home':
                window6.close()
                window1.un_hide()
                break
            

                
try:
    window.close()
except:
    pass
try:
    window1.close()
except:
    pass
try:
    window2.close()
except:
    pass
try:
    window3.close()
except:
    pass
try:
    window4.close()
except:
    pass

camera.release()

#Na janela 3 quando dou home, fecha tudo. ver pq isso acontece.#colocar um aviso para tirar os oculos na hora de tirar a foto