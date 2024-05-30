import cv2
import winsound
import threading
import time

def play_sound():
    winsound.PlaySound("C:/Windows/Media/chimes.wav", winsound.SND_FILENAME)
ultima_reproduccion = 0
delay = 2

camara = cv2.VideoCapture(0)
rostrosEntrenado = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

while(camara.isOpened()):
    ret,imagen=camara.read()
    gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    rostro = rostrosEntrenado.detectMultiScale(gray, 1.1, 5)
    for (x,y,w,h) in rostro:
       cv2.rectangle(imagen, (x,y), ((x+w),(y+h)),(0,255,255),2)
       if time.time()-ultima_reproduccion > delay:
           ultima_reproduccion = time.time()
           threading.Thread(target=play_sound).start()
    cv2.imshow("video",imagen)
    if cv2.waitKey(1) & 0XFF == ord("S"):
        break
  
          
camara.release()
cv2.destroyAllWindows()