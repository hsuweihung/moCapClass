#import library
import cv2
import mediapipe as mp
import pyautogui

#open the frame on the computer
cap =cv2.VideoCapture(0)#capture the video
hand_detector =mp.solutions.hands.Hands() #detect the hand

#to expend the moving area of the finger outside the frame
screen_width, screen_height = pyautogui.size()
index_y=0
vertical_movement=0

while True:
    _, frame=cap.read()
    frame=cv2.flip(frame, 1) #flip the landmark
    frame_height, frame_width, _= frame.shape
    rgb_frame =cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output =hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks #fetch the landmark of the finger
    drawing_utils = mp.solutions.drawing_utils
    
    if hands: #draw the finger
        for hand in hands:
            is_right_hand = hand.landmark[9].x < hand.landmark[5].x
            drawing_utils.draw_landmarks(frame, hand)
            landmarks=hand.landmark
            for id, landmarks in enumerate(landmarks):
                x=int(landmarks.x*frame_width)
                y=int(landmarks.y*frame_height)
                
                if id==8: #setting index
                    cv2.circle(img=frame, center=(x, y), radius=30, color=(255,0,0))
                    index_x =screen_width/frame_width*x
                    index_y=screen_height/frame_height*y
                    pyautogui.moveTo(index_x, index_y)#mouse moving with the finger
                    
                if id==4: #setting thumb
                    cv2.circle(img=frame, center=(x, y), radius=30, color=(255,0,0))
                    thumb_x =screen_width/frame_width*x
                    thumb_y=screen_height/frame_height*y
                    
                    #print ("outside:", abs(index_y-thumb_y))
                    #setting click event，when two finger are close enough
                    if abs(index_y-thumb_y) < 30:
                        pyautogui.click()
                        print("click")
                        pyautogui.sleep(1)   
                               
    cv2.imshow('NUI Mouse', frame)
    cv2.waitKey(1)

