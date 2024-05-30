import cv2
camara = cv2.VideoCapture(0)
rostrosEntrenado = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_upperbody.xml")
while(camara.isOpened()):
    ret,imagen=camara.read()
    gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    rostro = rostrosEntrenado.detectMultiScale(gray, scaleFactor=1.1,
            minNeighbors=5,
            minSize=(50, 50),
            maxSize=(400, 400))
    for (x,y,w,h) in rostro:
       cv2.rectangle(imagen, (x,y), ((x+w),(y+h)),(0,255,255),2)
       print("Hola") 
    cv2.imshow("video",imagen)
    if cv2.waitKey(1) & 0XFF == ord("S"):
        break
camara.release()
cv2.destroyAllWindows()