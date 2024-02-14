import cv2
from deepface import DeepFace

cam = cv2.VideoCapture(0)

while cam.isOpened():
    
    ret, frame = cam.read()
    
    if not ret:
        break
    
    if ret is True:
        cv2.imshow('gago', frame)
        
        if cv2.waitKey(25) == ord('q'):
            cam.release()
            break
        
cam.release()
cv2.destroyAllWindows()