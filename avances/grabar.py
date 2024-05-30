import cv2
captura = cv2.VideoCapture("C:/Users/aleco/Downloads/4C.mp4")
#salida = cv2.VideoWriter("videoGuardado.avi",cv2.VideoWriter_fourcc(*"XVID"),230.0,(600,600))

while (captura.isOpened()):
    ret,imagen=captura.read()
    if ret==True:
        cv2.imshow("video",imagen)
 #       salida.write(imagen)
        if cv2.waitKey(2000) & 0XFF == ord ("S"):
            break
        else: break
captura.release()
#salida.release()
cv2.destroyAllWindows()
