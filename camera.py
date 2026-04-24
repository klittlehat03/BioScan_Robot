#chat GPT

import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("error: could not open camera.")
    exit()
    
print("press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("failed to grab frame.")
        break
    
    cv2.imshow('live camera feed', frame)
    
    #press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
#Release resources
cap.release()
cv2.destroyAllWindows()
