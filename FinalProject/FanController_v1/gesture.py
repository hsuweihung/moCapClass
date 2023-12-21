import serial
import mediapipe as mp

mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands

ser = serial.Serial('COM7', 9600, timeout=1)


def control_fan(hand_landmarks, img):
    fingers_open = 0

    for finger_id in range(1, 5):
        if hand_landmarks.landmark[mpHands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP - finger_id].y:
            fingers_open += 1

    if fingers_open == 5:
        ser.write(b'5')
    elif fingers_open > 0:
        fan_speed = min(max(fingers_open, 1), 3)
        ser.write(str(fan_speed).encode())
    else:
        ser.write(b'0')