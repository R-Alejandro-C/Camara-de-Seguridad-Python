import cv2
captura = cv2.VideoCapture(0)

while(captura.isOpened()):
    ret,imagen=captura.read()
    if ret==True:
        flip = cv2.flip(imagen,1)
        cv2.imshow("video",flip)
        if cv2.waitKey(1) & 0XFF == ord("S"):
            break
captura.release()
cv2.destroyAllWindows()
