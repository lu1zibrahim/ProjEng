import cv2
import face_recognition as fr
import numpy as np
from datetime import datetime
import os

faces = []
nome = 'Luiz'

img = f'rostos/{nome}.jpg' #insira o nome do arquvio, e deixe ele na mesma pasta desse .py

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
    
    
encodeTrain = treinamento(img)
salvaEncode(encodeTrain, str(img.split(".")[0]))