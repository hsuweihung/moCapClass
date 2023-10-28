#install package in terminal
#pip3 install mediapipe
#pip3 install opencv-python

#import library
import mediapipe as mp
import cv2
import time
import math
import numpy as np

mpDraw = mp.solutions.drawing_utils #Call the drawing tool
mpHands = mp.solutions.hands #Call the hand tracking tool

#Setup handtracking module
hands = mpHands.Hands(  
    static_image_mode=False, #Image or Video (True: still image, False: stream mode)
    model_complexity=0,#0->compact model(fast speed)，1->full mode(slow speed)
    max_num_hands=2,  #How many hands are allowed to be recognized
    min_detection_confidence=0.7, #confidence for hand detection
    min_tracking_confidence=0.5 #confidence for hand tracking
    )
AngleTH=130 #threshold(TH) angle: the joint in range of motion
def findAngleF(a,b,c):    
    ang = math.degrees(math.atan2(c[2]-b[2], c[1]-b[1]) - math.atan2(a[2]-b[2], a[1]-b[1]))
    if ang<0 :
      ang=ang+360
    if ang >= 360- ang:
        ang=360-ang
    return round(ang,2)

#Start Hand Gesture Tracking
cap = cv2.VideoCapture(0)
while cap.isOpened(): #Is camera open or not
    stime=time.time()
    ret, frame = cap.read() #read camera data
    h, w, c = frame.shape  #get resolution(width/height) of the camera
    frame=cv2.flip(frame,1) #flip image：-1:up and down、0: up and down, left and right、1:  left and right
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #convert color channel from BGR(opencv) to RGB(mediapipe)
    results = hands.process(imgRGB) #tracking hands and get the results
       
    if results.multi_hand_landmarks: #If there is any hand available
        for i in range(len(results.multi_handedness)): #get the numbers of detected hands
            thisHandType=results.multi_handedness[i].classification[0].label #get properties of the detected hand          
            thisHand=results.multi_hand_landmarks[i] #get hand label information 
            mpDraw.draw_landmarks(frame, thisHand, mpHands.HAND_CONNECTIONS) #draw tools
            thisHandLMList = []
            for id, lm in enumerate(thisHand.landmark): #id=number,lm=coordinate                  
                thisHandLMList.append([id, lm.x, lm.y,lm.z])
                hx, hy = int(lm.x * w), int(lm.y * h) #get coordinate of the joint
                cv2.circle(frame, (hx, hy), 5, (255, 0, 0), cv2.FILLED)  #make circles with blue color
                cv2.putText(frame,str(id),(hx,hy), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
                if id==0:
                    cv2.putText(frame,thisHandType,(hx,hy-30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)            
            finger=[0,0,0,0,0]
            if (findAngleF(thisHandLMList[0],thisHandLMList[3],thisHandLMList[4])>AngleTH):
                finger[0]=1
            if (findAngleF(thisHandLMList[0],thisHandLMList[6],thisHandLMList[8])>AngleTH):
                finger[1]=1
            if (findAngleF(thisHandLMList[0],thisHandLMList[10],thisHandLMList[12])>AngleTH):
                finger[2]=1
            if (findAngleF(thisHandLMList[0],thisHandLMList[14],thisHandLMList[16])>AngleTH):
                finger[3]=1
            if (findAngleF(thisHandLMList[0],thisHandLMList[18],thisHandLMList[20])>AngleTH):
                finger[4]=1
            #print(finger)

            #-----------------Recognizing hand gestures------------------------
            text=""#     Thumb,Index,Middle,Ring,Little finger
            if (finger==[1,0,0,0,0]):
                text="Good"
            if (finger==[0,0,1,1,1]):
                text="OK"            
            if (finger==[1,1,1,1,1]):
                text="Hi"           
            if (finger==[0,1,1,0,0]):
                text="Ya" 
            if (finger==[1,0,0,0,1]):
                text="Rock" 
            if (finger==[1,0,1,0,1]):
                text="Airplane"
            if (finger==[1,1,0,0,1]):
                text="SPIDER-MAN"
            #           Image   text   coordinate       font style   font size   font color  thickness
            cv2.putText(frame, text, (0, 200), cv2.FONT_HERSHEY_PLAIN, 5  , (255, 0, 0), 5) #put text to the screen

    etime=time.time()
    fps=round(1/(etime-stime),2)
    cv2.putText(frame,"FPS:" + str(fps),(10,50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
    cv2.imshow('Webcam',frame) #display results on the screen
    key=cv2.waitKey(1) #waitting for user's inputs
    if key==ord('a'):   # 'a': capture photo
        cv2.imwrite('webcam.jpg',frame) # save file
    if key==ord('q'):  #'q': quit
        break
cap.release()
cv2.destroyAllWindows()