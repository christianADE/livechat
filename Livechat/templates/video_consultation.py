import cv2

def consultation_video():
    cap = cv2.VideoCapture(0)

    while(True):
        ret, frame = cap.read()
        cv2.imshow('Consultation en cours', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

consultation_video()
