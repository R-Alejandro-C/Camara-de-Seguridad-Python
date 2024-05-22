import cv2
captura = cv2.VideoCapture(1)
i = 0
while True:
    ret,imagen=captura.read()
    if not ret: break
    gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    flipp = cv2.flip(imagen,1)
    if i == 20:
      bgGray = gray
    if i>20:
      dif = cv2.absdiff(gray, bgGray)
      _, th = cv2.threshold(dif, 20, 255, cv2.THRESH_BINARY)
      cnts, _= cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      diff= cv2.flip(dif,1)
#      cv2.imshow("dif",th)
      for c in cnts:
        area = cv2.contourArea(c)
        if area > 3000:
          x,y,w,h = cv2.boundingRect(c)
          cv2.rectangle(imagen, (x,y), ((x+w),(y+h)),(0,255,255),2)
    cv2.imshow("video",imagen)
    i = i+1
    if cv2.waitKey(1) & 0XFF == ord("S"):
        break



captura.release()
cv2.destroyAllWindows()