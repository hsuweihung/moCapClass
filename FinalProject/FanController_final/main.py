import cv2
import serial
import mediapipe as mp
from gesture import control_fan

# Initialize MediaPipe hand model
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=1, min_detection_confidence=0.5)
mpDraw = mp.solutions.drawing_utils


def main():
    cap = cv2.VideoCapture(0)

    try:
        while cap.isOpened():
            ret, img = cap.read()
            if not ret:
                continue

            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)

            if results.multi_hand_landmarks:
                for handLms, handInfo in zip(results.multi_hand_landmarks, results.multi_handedness):
                    # Get hand type (left or right)
                    handType = handInfo.classification[0].label
                    mpDraw.draw_landmarks(
                        img, handLms, mpHands.HAND_CONNECTIONS)
                    fingers_open = control_fan(handLms, handType)

                    # Swap left and right labels
                    display_hand_type = 'Right' if handType == 'Left' else 'Left'

                    cv2.putText(img, f'{display_hand_type} Hand, Fingers: {fingers_open}', (
                        10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

            cv2.imshow("Image", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
