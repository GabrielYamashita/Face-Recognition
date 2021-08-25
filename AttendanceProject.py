# Bibliotecas Usadas
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

# Settings
path = './ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)

# Pegando os Nomes de cada Foto
for cl in myList:
   curImg = cv2.imread(f'{path}/{cl}')
   images.append(curImg)
   classNames.append(os.path.splitext(cl)[0])

# Fazendo o Encoding
def findEncodings(images):
   encodeList = []
   for img in images:
      img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      encode = face_recognition.face_encodings(img)[0]
      encodeList.append(encode)

   return encodeList

encodeListKnown = findEncodings(images)
print('Encoding Complete')

# Salvando o Nomes Novos no csv
def markAttendance(name):
   with open('./Attendance.csv', 'r+') as f:
      myDataList = f.readlines()
      nameList = []
      
      for line in myDataList:
         entry = line.split(',')
         nameList.append(entry[0])

      if name not in nameList:
         now = datetime.now()
         dtString = now.strftime('%H:%M:%S')
         f.writelines(f'\n{name},{dtString}')

# Configurações da Câmera
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Loop Principal
while True:
   success, img = cap.read()
   imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
   imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

   # Obtendo Informações
   facesCurrentFrame = face_recognition.face_locations(imgS)
   encodesCurrentFrame = face_recognition.face_encodings(imgS, facesCurrentFrame)

   # Identificando o Match das Faces
   for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
      matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
      faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)
      # print(faceDistance)
      matchIndex = np.argmin(faceDistance)

      # Checando o nome e colocando na Imagem
      if matches[matchIndex]:
         name = classNames[matchIndex].upper()
         # print(name)
         y1, x2, y2, x1 = faceLoc
         cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
         cv2.rectangle(img, (x1,y2-35), (x2,y2), (0,255,0), cv2.FILLED)
         cv2.putText(img, name, (x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
         markAttendance(name)

   # Inicializando a Câmera
   cv2.imshow('Webcam', img)
   cv2.waitKey(1)
