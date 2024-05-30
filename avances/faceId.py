import cv2
import os

dataPath = "C:/Users/aleco/Documents/GitHub/python/openCV/Practica1/rostros"
imagePath = os.listdir(dataPath)
print("iamgepath",imagePath)

#entrenamiento=cv2.face.EigenFaceRecognizer_create()
entrenamiento = cv2.face.LBPHFaceRecognizer_create()
entrenamiento.read("LBPHFaceRecognizer.xml")

camara = cv2.VideoCapture(0)
rostrosEntrenado = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
while(camara.isOpened()):
    ret,imagen=camara.read()
    gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    auximagen = gray.copy()
    rostro = rostrosEntrenado.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in rostro:
         capturado = auximagen[y:y+h,x:x+w]
         capturado = cv2.resize(capturado,(150,150),interpolation=cv2.INTER_CUBIC)
         result = entrenamiento.predict(capturado)
         cv2.putText(imagen,"{}".format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
         
         if result[1]<61:
            cv2.putText(imagen,"{}".format(imagePath[result[0]]),(x,y-25),1,1.3,(255,255,0),1,cv2.LINE_AA)
         else:
             cv2.putText(imagen,"Rostro no detectado",(x,y-25),1,1.3,(255,255,0),1,cv2.LINE_AA)
             

    cv2.imshow("video",imagen)
    if cv2.waitKey(1) & 0XFF == ord("S"):
        break
camara.release()
cv2.destroyAllWindows()