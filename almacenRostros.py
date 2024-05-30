import cv2
import os
import sys
import subprocess

def entrenar():    
    subprocess.Popen(['python', 'trainingFaces.py'])


def guardarNuevoRostro(nombreCarpeta):
    ruta1 = "rostros"
    if not os.path.exists(ruta1):
        print("Carpeta creada", ruta1)
        os.makedirs(ruta1)

    rutaunida = os.path.join(ruta1,nombreCarpeta)

    if not os.path.exists(rutaunida):
        print("Carpeta creada", rutaunida)
        os.makedirs(rutaunida)

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
            if count<100:
                cv2.imwrite(os.path.join(rutaunida, "ROSTRO_{}.jpg".format(count)), capturado)
                cv2.imshow("video",capturado)
                count = count+1
            
        cv2.rectangle(imagen, (10,5), (420,25),(0,255,255),-1)   
        cv2.imshow("imagen",imagen)
        if cv2.waitKey(1) & 0XFF  == ord("S"):
            break
        
    camara.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        guardarNuevoRostro(sys.argv[1])
        entrenar()
    else:
        print("Por favor, proporciona el nombre de la carpeta.")