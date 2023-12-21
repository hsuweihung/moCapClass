import cv2
import mediapipe as mp
from gesture import control_fan

mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands

hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=0,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)
fan_open = False

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, hand_landmarks,
                                  mpHands.HAND_CONNECTIONS)
            control_fan(hand_landmarks, img)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
