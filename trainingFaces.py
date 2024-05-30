import cv2 
import os
import numpy as np

dataPath = "C:/Users/aleco/Documents/GitHub/python/openCV/Practica1/rostros"
listaPersonas = os.listdir(dataPath)

labels = []
facesData = []
label= 0

for nameDir in listaPersonas:
    personPath = dataPath + "/" + nameDir
    print("scan")

    for fileName in os.listdir(personPath):
        print("rostro: ",dataPath + "/" + fileName)
        labels.append(label)
        facesData.append(cv2.imread(personPath+"/"+fileName,0))
        image = cv2.imread(personPath+"/"+fileName,0)
    #    cv2.imshow("image", image)
     #   cv2.waitKey(10)
label = label+1
#entrenamiento=cv2.face.EigenFaceRecognizer_create()
#entrenamiento = cv2.face.FisherFaceRecognizer_create()
entrenamientoL_BPHFaceRecognizer = cv2.face.LBPHFaceRecognizer_create()
print("Entrenando....")
#entrenamiento.train(facesData,np.array(labels))
#entrenamiento.train(facesData,np.array(labels))
entrenamientoL_BPHFaceRecognizer.train(facesData,np.array(labels))
#entrenamiento.write("modeloEigenFace.xml")
#entrenamiento.write("FisherFaceRecognizer.xml")
entrenamientoL_BPHFaceRecognizer.write("LBPHFaceRecognizer.xml")
print("entrenamiento exitoso")
#cv2.destroyAllWindows()