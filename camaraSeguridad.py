import cv2
import os
import winsound
import threading
import time
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib
from email.mime.image import MIMEImage

# Crear carpeta para almacenar imágenes completas detectadas si no existe
if not os.path.exists("Rostro encontrado"):
    print("Carpeta creada")
    os.makedirs("Rostro encontrado")

# Cargar variables de entorno
load_dotenv()
password = os.getenv("PASSWORD")
email_from = "kailer.3000.11@gmail.com"
email_to = "kailer.3000.11@gmail.com"

# Configuracion de contenido del correo electrónico
subject = "¡Te están robando! ... Tal vez ..."
body = """Es posible que alguien esté en tu domicilio"""

def enviar_correo():
    em = EmailMessage()
    em["From"] = email_from
    em["To"] = email_to
    em["Subject"] = subject
    em.set_content(body)

    # Adjuntar imágenes de la carpeta "Rostro encontrado"
    folder = "Rostro encontrado"
    for filename in os.listdir(folder):
        if filename.endswith(".jpg"):
            filepath = os.path.join(folder, filename)
            with open(filepath, 'rb') as f:
                img_data = f.read()
            em.add_attachment(img_data, maintype='image', subtype='jpeg', filename=filename)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_to, password)
        smtp.sendmail(email_to, email_from, em.as_string())

detener = False

# Cargar datos de entrenamiento para reconocimiento facial
dataPath = "C:/Users/aleco/Documents/GitHub/python/openCV/Practica1/rostros"
imagePath = os.listdir(dataPath)
print("imagePath", imagePath)

def play_sound():
    global detener
    winsound.PlaySound("C:/Windows/Media/chimes.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
    while not detener:
        time.sleep(0.1)
    winsound.PlaySound(None, winsound.SND_PURGE)

ultima_reproduccion = 0
delay = 2
sonido_thread = None

# Temporizador para el envío de correos electrónicos
ultima_envio_correo = 0
intervalo_correo = 10  # Enviar correo cada 10 segundos

# Cargar modelo de reconocimiento facial pre-entrenado
entrenamiento = cv2.face.LBPHFaceRecognizer_create()
entrenamiento.read("LBPHFaceRecognizer.xml")

# Inicializar cámara y detector de rostros
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
        _, th = cv2.threshold(dif, 40, 255, cv2.THRESH_BINARY)
        cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            area = cv2.contourArea(c)
            if area > 9000:
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
        
        if result[1] < 72:
            cv2.putText(imagen, "{}".format(imagePath[result[0]]), (x, y - 25), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
            detener = True
            if sonido_thread and sonido_thread.is_alive():
                sonido_thread.join()
                
        else:
            cv2.putText(imagen, "Persona", (x, y - 25), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
            cv2.imwrite("Rostro encontrado/IMAGEN_{}.jpg".format(i), imagen)  # Guardar la imagen completa
            
            # Enviar correo si ha pasado el intervalo definido
            if time.time() - ultima_envio_correo > intervalo_correo:
                ultima_envio_correo = time.time()
                threading.Thread(target=enviar_correo).start()
       
    i += 1
    cv2.imshow("video", imagen)
    if cv2.waitKey(1) & 0xFF == ord("S"):
        detener = True
        if sonido_thread and sonido_thread.is_alive():
            sonido_thread.join()
        break

camara.release()
cv2.destroyAllWindows()
