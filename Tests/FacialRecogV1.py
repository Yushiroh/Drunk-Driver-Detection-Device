import threading
import cv2
from deepface import DeepFace



cap = cv2.VideoCapture(0)


counter = 0

face_match = False

reference_img = cv2.imread('reference.jpg')

def checkFace(frame):
    print("Checking Face")
    global face_match
    try:
        if DeepFace.verify(frame, reference_img.copy())['verified']:
            face_match = True
        else:
            face_match = False
    except ValueError:
        face_match = False


while True:
    ret, frame = cap.read()


    if ret:
        if counter % 30 == 0:

            try:
                threading.Thread(target= checkFace, args = (frame.copy(),)).start()
            except ValueError:
                pass

        counter += 1

        if face_match:
            cv2.putText(frame, "MATCH", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "NO MATCH", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        cv2.imshow("Video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cv2.destroyAllWindows()
print("WAZUPPPP")