import serial
import mediapipe as mp

mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands

ser = serial.Serial('/dev/cu.usbserial-140', 9600, timeout=1)


def control_fan(hand_landmarks, hand_type):
    fingers_open = 0

    # Check if each finger is open
    # Adjust thumb detection based on hand type (left or right)
    if hand_type == 'Right':
        if hand_landmarks.landmark[mpHands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mpHands.HandLandmark.THUMB_IP].x:
            fingers_open += 1
    else:  # Left hand
        if hand_landmarks.landmark[mpHands.HandLandmark.THUMB_TIP].x > hand_landmarks.landmark[mpHands.HandLandmark.THUMB_IP].x:
            fingers_open += 1

    # Other fingers
    for finger in [mpHands.HandLandmark.INDEX_FINGER_TIP, mpHands.HandLandmark.MIDDLE_FINGER_TIP, mpHands.HandLandmark.RING_FINGER_TIP, mpHands.HandLandmark.PINKY_TIP]:
        if hand_landmarks.landmark[finger].y < hand_landmarks.landmark[finger - 2].y:
            fingers_open += 1

    ser.write(str(fingers_open).encode())
    return fingers_open
