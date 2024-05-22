import cv2
import os
if not os.path.exists("Rostro encontrado"):
    print("Carpeta creada")
    os.makedirs("Rostro encontrado")

camara = cv2.VideoCapture(0, cv2.CAP_DSHOW)
rostrosEntrenado = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

count = 0

while(camara.isOpened()):
    ret,imagen=camara.read()
    imagen = cv2.flip(imagen,1)
    gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    auximagen = imagen.copy()
    rostro = rostrosEntrenado.detectMultiScale(gray, 1.1, 5)

    for (x,y,w,h) in rostro:
       cv2.rectangle(imagen, (x,y), ((x+w),(y+h)),(129,0,255),2)
       capturado = auximagen[y:y+h,x:x+w]
       capturado = cv2.resize(capturado,(150,150),interpolation=cv2.INTER_CUBIC)
       if count<5000:
        cv2.imwrite("Rostro encontrado/ROSTRO_{}.jpg".format(count),capturado)
        cv2.imshow("video",capturado)
        count = count+1
    cv2.rectangle(imagen, (10,5), (420,25),(0,255,255),-1)   
    cv2.imshow("imagen",imagen)
    if cv2.waitKey(1) & 0XFF == ord("S"):
        break
camara.release()
cv2.destroyAllWindows()