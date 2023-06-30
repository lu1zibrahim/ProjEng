import PySimpleGUI as sg      
import cv2
import numpy as np
import pandas as pd
import face_recognition as fr
from datetime import datetime
import os
import csv
import operator
from time import sleep

'''
    Example of wizard-like PySimpleGUI windows
'''
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

if os.path.exists('registro_saida.csv'):
    inicio_saida = pd.read_csv('registro_saida.csv')
    registros_saida = inicio_saida.values.tolist()
    print(registros_saida)
else:
    print('not')
    registros_saida = []

registros_entrada = []
nomes_entrada = []




def sort_table(table, cols, descending=False):
    """ sort a table by multiple columns
        table: a list of lists (or tuple of tuples) where each inner list
                represents a row
        cols:  a list (or tuple) specifying the column numbers to sort by
                e.g. (1,0) would sort by column 1, then by column 0
    """

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
              [sg.Button("", image_filename='UI/Icons/acessar_camera2.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Janela_verificar"),
              sg.Button("", image_filename='UI/Icons/cadastrar_usuario.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Janela_cadastrar"),
              sg.Button("", image_filename='UI/Icons/acessar_logs_2.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Janela_log")],
              ], justification='center')]
              ]

    return sg.Window('Home', layout,size=(1024,800),resizable=True,  finalize=True)


def make_window2():
    sg.theme('Black')
    layout = [[sg.Column([
        [sg.Text('Camera', size=(40, 1), justification='center', font='Helvetica 20')], # Texto para a Camera
              [sg.Image(filename='', key='image')], # Local para a camera
              [sg.Button("", image_filename='UI/Icons/ligar_camera_final.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Ligar Camera"),
               sg.Button("", image_filename='UI/Icons/verificar_final.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Verificar")],
              [sg.Button("", image_filename='UI/Icons/PaginaInicial.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Home")],
                 ], justification='center')]
               ]
    
    
    
    return sg.Window('Janela Verificar', layout,size=(800,800),resizable=True, finalize=True)


def make_window3():
    sg.theme('Black')
    layout = [[sg.Column([
            [sg.Image('UI/Icons/nome_funcionario.png')], # Entrada de nome do funcionario - Campo de visualização
              [sg.Input(key='-IN-', size=(40,2), justification='center', font='Helvetica 15')], # Entrada de nome do funcionario - Campo de Input
              [sg.Image(filename='', key='image')],# Local para a camera
              [sg.Button("", image_filename='UI/Icons/ligar_camera_final.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Ligar Camera"), # Contém os campos de botões de acionamento
               sg.Button("", image_filename='UI/Icons/tirar_foto_final.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Tirar Foto"), 
               sg.Button("", image_filename='UI/Icons/cadastrar_final.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Cadastrar")],
              [sg.Button("", image_filename='UI/Icons/PaginaInicial.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Home")],
    ], justification='center')]
               ]
    return sg.Window('Janela Cadastrar', layout, size=(800,800), resizable=True, finalize=True)
    # Criação da janela


def make_window4():
    sg.theme('Black')
    # CSV_FILE = sg.popup_get_file('CSV File to Display', file_types=(("CSV Files", "*.csv"),), initial_folder=os.path.dirname(__file__), history=True)
    # if CSV_FILE is None:
    #     sg.popup_error('Canceling')
    #     exit()
    data, header_list = read_csv_file('registro_saida.csv')
    layout = [  [sg.Text('Click a heading to sort on that column or enter a filter and click a heading to search for matches in that column')],
                [sg.Text(f'{len(data)} Records in table', font='_ 18')],
                [sg.Text(k='-RECORDS SHOWN-', font='_ 18')],
                [sg.Text(k='-SELECTED-')],
                # [sg.T('Filter:'), sg.Input(k='-FILTER-', focus=True, tooltip='Not case sensative\nEnter value and click on a col header'),
                #  sg.B('Reset Table', tooltip='Resets entire table to your original data'),
                #  sg.Checkbox('Sort Descending', k='-DESCENDING-'), sg.Checkbox('Filter Out (exclude)', k='-FILTER OUT-', tooltip='Check to remove matching entries when filtering a column'), sg.Push()],
                [sg.Table(values=data, headings=header_list, max_col_width=25,
                        auto_size_columns=True, display_row_numbers=True, vertical_scroll_only=True,
                        justification='right', num_rows=50,
                        key='-TABLE-', selected_row_colors='red on yellow', enable_events=True,
                        expand_x=True, expand_y=True,
                        enable_click_events=True)],
                [sg.Sizegrip()],
                [sg.Button("", image_filename='UI/Icons/PaginaInicial.png', button_color=(sg.theme_background_color(),sg.theme_background_color()),font=('Bookman Old Style', 1),border_width=0,key="Home")]]
    return sg.Window('CSV Table Display', layout,layout, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT,  resizable=True, finalize=True)


window1, window2, window3, window4 = make_window1(), None, None, None

while True:
    window, event, values = sg.read_all_windows()
    if window == window1 and event in (sg.WIN_CLOSED, 'Exit'):
        break

    if window == window1:
        if event == 'Janela_verificar':
            window1.hide()
            window2 = make_window2()
        elif event == 'Janela_cadastrar':
            window1.hide()
            window3 = make_window3()
        elif event == 'Janela_log':
            window1.hide()
            window4 = make_window4()

    if window == window2:
        recording = True
        verificando = False

        while True: # Loop principal de leitura dos valores.
            event, values = window.read(timeout=20)
            if event == 'Sair' or event == sg.WIN_CLOSED:
                reg_saida = pd.DataFrame(registros_saida, columns =['Nome', 'Entrada', 'Saida','Duracao'])
                reg_saida.to_csv('registro_saida.csv', index=False)
                break

            elif event == 'Ligar Camera':
                verificando = False
                recording = True

            elif event == 'Home':
                reg_saida = pd.DataFrame(registros_saida, columns =['Nome', 'Entrada', 'Saida','Duracao'])
                reg_saida.to_csv('registro_saida.csv', index=False)
                window2.close()
                window1.un_hide()

            elif event == 'Parar':
                recording = False
                verificando = False
                # img = np.full((480, 640), 255)
                # # this is faster, shorter and needs less includes
                # imgbytes = cv2.imencode('.png', img)[1].tobytes()
                # window['image'].update(data=imgbytes)
            
            elif event == "Verificar": # Inicia o mapeamento da imagem do rosto do funcionario
                recording = False
                verificando = True

            elif recording: # Esta condição verifica se foi pressionado "Ligar a Camera" assim ela liga a leitura do OpenCV e projeta na tela
                ret, frame = camera.read()
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
                                    print('1')
                                    try: 
                                        detect = frame
                                        cv2.rectangle(detect, (loc_x, loc_y), (loc_x+loc_w, loc_y+loc_h) ,(0,255,0),2)
                                        org = (loc_x, loc_y)
                                        cv2.putText(detect, nome, org , font, fontScale, color, thickness, cv2.LINE_AA, False)
                                        print('2')

                                        if len(registros_entrada) == 0:
                                            """
                                            Primeiramente conferir se a lista estiver vazia, caso esteja, irá inserir o primeiro usuário
                                            """
                                            agora = datetime.now()
                                            registros_entrada.append([nome,agora])
                                            print(registros_entrada)
                                            print('3')
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
                                        recording = False
                                        sg.popup(f'Usuario Liberado, Bem Vindo(a) - {nome}')
                                        print('4')
                                        # print(registros_entrada)
                                        # print(nomes_entrada)
                                        #sleep(2)
                                        comparacao = False
                                        break
                                    except:
                                        print('erro ao inserir credenciais...')
                                        comparacao = False
                                        print('5')
                                        aux_compare += 1
                                        pass
                                else:
                                    print('6')
                                    aux_compare += 1
                        print('7')
                        
                        break
                                
                    print('8')
                    aux_detect += 1 
                    if aux_detect == 5 :
                        print("NÃO FOI POSSIVEL IDENTIFICAR")
                        verificando = False
                        recording = True

    if window == window3:
            camera = cv2.VideoCapture(0) # Identificando a Camera
            recording = True
            picture = False
            while True: # Loop principal de leitura dos valores.
                event, values = window.read(timeout=20)
                check_nome = bool(nome) # Verifica se o input de nome está vazio
                if event == 'Sair' or event == sg.WIN_CLOSED:
                    break

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
                elif event == 'Home':
                    window3.close()
                    window1.un_hide()

                elif recording: # Esta condição verifica se foi pressionado "Ligar a Camera" assim ela liga a leitura do OpenCV e projeta na tela
                    ret, frame = camera.read()
                    imgbytes = cv2.imencode('.png', frame)[1].tobytes()
                    window['image'].update(data=imgbytes)
                    nome = values['-IN-']
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
                    except IndexError: # Caso não o face_recognition não identificar um rosto ele vai retornar IndexError Out of Range, então nos preparamos para este erro
                        os.chdir('..')
                        sg.popup('Não foi possível cadastrar o rosto, favor tentar novamente')
                        recording = True

    if window == window4:
        window.bind("<Control_L><End>", '-CONTROL END-')
        window.bind("<End>", '-CONTROL END-')
        window.bind("<Control_L><Home>", '-CONTROL HOME-')
        window.bind("<Home>", '-CONTROL HOME-')
        #original_data = data        # save a copy of the data
        csv.field_size_limit(2147483647)        # enables huge tables
        print('aqui?')
        while True:
            event, values = window.read()
            # print(event, values)
            if event in (sg.WIN_CLOSED, 'Sair'):
                break
            if values['-TABLE-']:           # Show how many rows are slected
                window['-SELECTED-'].update(f'{len(values["-TABLE-"])} rows selected')
            else:
                window['-SELECTED-'].update('')
            #if event[0] == '-TABLE-':
            # if isinstance(event, tuple):
                # filter_value = values['-FILTER-']
                # # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
                # if event[0] == '-TABLE-':
                #     if event[2][0] == -1 and event[2][1] != -1:  # Header was clicked and wasn't the "row" column
                #         col_num_clicked = event[2][1]
                        # if there's a filter, first filter based on the column clicked
                        # if filter_value not in (None, ''):
                        #     filter_out = values['-FILTER OUT-']     # get bool filter out setting
                        #     new_data = []
                        #     for line in data:
                        #         if not filter_out and (filter_value.lower() in line[col_num_clicked].lower()):
                        #             new_data.append(line)
                        #         elif filter_out and (filter_value.lower() not in line[col_num_clicked].lower()):
                        #             new_data.append(line)
                        #     data = new_data
                        # new_table = sort_table(data, (col_num_clicked, 0), values['-DESCENDING-'])
                        # window['-TABLE-'].update(new_table)
                        # data = new_table
                        # window['-RECORDS SHOWN-'].update(f'{len(new_table)} Records shown')
                        # window['-FILTER-'].update('')           # once used, clear the filter
                        # window['-FILTER OUT-'].update(False)  # Also clear the filter out flag
            # elif event == 'Reset Table':
            #     data = original_data
            #     window['-TABLE-'].update(data)
            #     window['-RECORDS SHOWN-'].update(f'{len(data)} Records shown')
            # elif event == '-CONTROL END-':
            #     window['-TABLE-'].set_vscroll_position(100)
            # elif event == '-CONTROL HOME-':
            #     window['-TABLE-'].set_vscroll_position(0)
            # elif event == 'Edit Me':
            #     sg.execute_editor(__file__)
            # elif event == 'Version':
            #     sg.popup_scrolled(__file__, sg.get_versions(), location=window.current_location(), keep_on_top=True, non_blocking=True)
            if event == 'Home':
                window4.close()
                window1.un_hide()

camera.release()
window.close()