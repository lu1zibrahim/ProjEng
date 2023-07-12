import cv2
import face_recognition as fr
import numpy as np
from datetime import datetime
import os
from time import sleep


camera = cv2.VideoCapture(0)
rodando = True
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

#rodando = False
while rodando:
    aux_compare = 0
    status, frame = camera.read()
    frame = cv2.resize(frame, (640,480), interpolation = cv2.INTER_AREA)
    
    aux_detect = 0
    aux_sleep_box = 0
    if cv2.waitKey(1) & 0xff == ord('d'):
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

                                

                                # if nome in nomes_entrada:
                                #     registros_saida.append([nome, agora])
                                #     index_nome = nomes_entrada.index(nome)
                                #     agora = datetime.now()
                                #     tempo_permanencia = agora - (registros_entrada[index_nome][1])
                                #     print("SAIDA REGISTRADA: "+nome+" - TEMPO DE PERMANENCIA: "+str(tempo_permanencia))

                                #     pass
                                # else:
                                #     agora = datetime.now()
                                #     nomes_entrada.append(nome)
                                #     registros_entrada.append([nome, agora])
                                

                                print("ACESSO LIBERADO: "+str(nome))
                                # print(registros_entrada)
                                # print(nomes_entrada)
                                sleep(2)
                                
                                break
                            except:
                                print('erro ao inserir credenciais...')
                                comparacao = False
                                pass
                        else:
                            aux_compare = aux_compare + 1

                
                break

            aux_detect = aux_detect + 1 
            if aux_detect == 5 :
                print("NÃO FOI POSSIVEL IDENTIFICAR")          
    if not status or cv2.waitKey(1) & 0xff == ord('q'):
        rodando = False
        
    cv2.imshow('Janela_cam', frame)
    #print("aux_sleep_box = "+str(aux_sleep_box))


camera.release()
cv2.destroyAllWindows()