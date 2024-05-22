import cv2
import os
import winsound
import threading
import time

# Variable de control para detener el sonido
detener = False

# Ruta a los datos de rostros
dataPath = "C:/Users/aleco/Documents/GitHub/python/openCV/Practica1/rostros"
imagePath = os.listdir(dataPath)
print("imagePath", imagePath)

# Función para reproducir el sonido
def play_sound():
    global detener
    winsound.PlaySound("C:/Windows/Media/chimes.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
    while not detener:
        time.sleep(0.1) 
    winsound.PlaySound(None, winsound.SND_PURGE)

ultima_reproduccion = 0
delay = 2
sonido_thread = None

# Inicializar el reconocimiento facial
entrenamiento = cv2.face.EigenFaceRecognizer_create()
entrenamiento.read("modeloEigenFace.xml")
i = 0
camara = cv2.VideoCapture(0)
rostrosEntrenado = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

while camara.isOpened():
    ret, imagen = camara.read()
    if not ret:
        break
    gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    auximagen = gray.copy()
    rostro = rostrosEntrenado.detectMultiScale(gray, 1.3, 5)
    flipp = cv2.flip(imagen, 1)
    
    if i == 20:
        bgGray = gray
    if i > 20:
        dif = cv2.absdiff(gray, bgGray)
        _, th = cv2.threshold(dif, 20, 255, cv2.THRESH_BINARY)
        cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            area = cv2.contourArea(c)
            if area > 3000:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(imagen, (x, y), (x + w, y + h), (0, 255, 255), 2)
                if time.time() - ultima_reproduccion > delay:
                    ultima_reproduccion = time.time()
                    if sonido_thread and sonido_thread.is_alive():
                        detener = True
                        sonido_thread.join()
                    detener = False
                    sonido_thread = threading.Thread(target=play_sound)
                    sonido_thread.start()

    for (x, y, w, h) in rostro:
        capturado = auximagen[y:y + h, x:x + w]
        capturado = cv2.resize(capturado, (150, 150), interpolation=cv2.INTER_CUBIC)
        result = entrenamiento.predict(capturado)
        cv2.putText(imagen, "{}".format(result), (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
        
        if result[1] < 7000:
            cv2.putText(imagen, "{}".format(imagePath[result[0]]), (x, y - 25), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
            detener = True
            if sonido_thread and sonido_thread.is_alive():
                sonido_thread.join()
        else:
            cv2.putText(imagen, "Rostro no detectado", (x, y - 25), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
    
    i += 1
    cv2.imshow("video", imagen)
    if cv2.waitKey(1) & 0xFF == ord("S"):
        detener = True
        if sonido_thread and sonido_thread.is_alive():
            sonido_thread.join()
        break

camara.release()
cv2.destroyAllWindows()
