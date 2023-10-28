#install package in terminal
#pip3 install mediapipe
#pip3 install opencv-python
#pip3 install playsound==1.2.2
#pip3 

#import library
import mediapipe as mp
import cv2
import time
import math
import numpy as np
import random
#from playsound import playsound
#import playsound

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

#Load object image (white background can be removed)
ObjSizeX,ObjSizeY=80,80
BucketSizeX,BucketSizeY=180,80
Obj = cv2.resize(cv2.imread('l.png'),(ObjSizeX,ObjSizeY)) #Object image
#Load basket image
Bucket = cv2.resize(cv2.imread('b.png'),(BucketSizeX,BucketSizeY)) #Object image
#Grabbing Status
catchObj=False
#Whether to generate a New Object
NewObj=True
#Obj Starting Position
x,y=0,0
#Score
Score=0


AngleTH=130 #threshold(TH) angle: the joint in range of motion
def findAngleF(a,b,c):    
    ang = math.degrees(math.atan2(c[2]-b[2], c[1]-b[1]) - math.atan2(a[2]-b[2], a[1]-b[1]))
    if ang<0 :
      ang=ang+360
    if ang >= 360- ang:
        ang=360-ang
    return round(ang,2)

#Drawing: Placing the object at a specific position on the background, removing the white border
def addPng(ax,ay,bg,png):
    global NewObj
    pngY,pngX,channels = png.shape        
    bgY,bgX,channels = bg.shape
    if (ax+pngX<=bgX and ax>=0) and (ay+pngY<=bgY and ay>=0):
        roi = bg[ay:ay+pngY, ax:ax+pngX ] #Placement Position
        #1. Create a black PNG portion as a mask
        pnggray = cv2.cvtColor(png,cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(pnggray, thresh=230, maxval=255, type=cv2.THRESH_BINARY) #Less than thresh becomes 0, the rest become maxval.
        mask_inv = cv2.bitwise_not(mask) #Inverse
        #cv2.imshow('mask',mask_inv)
        #cv2.waitKey(0)
        #2.get the background area
        bg_roi = cv2.bitwise_and(roi,roi,mask = mask) # Extract the remaining background
        #cv2.imshow('mask',bg_roi)
        #cv2.waitKey(0)
        #3.get the Logo area
        png_roi = cv2.bitwise_and(png,png,mask = mask_inv) #Retrieve the actual display area
        #cv2.imshow('mask',png_roi)
        #cv2.waitKey(0)
        #4.making the final presenation
        dst = cv2.add(bg_roi,png_roi)
        bg[ay:ay+pngY, ax:ax+pngX ] = dst
        return bg
    else:
        NewObj=True
        return bg

#Detecting Palm Status
def fist(img):
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #convert color channel from BGR(opencv) to RGB(mediapipe)
    h, w, c = frame.shape #get resolution(width/height) of the camera
    results = hands.process(imgRGB)  #tracking hands and get the results

    if results.multi_hand_landmarks: #If there is any hand available
        for i in range(len(results.multi_handedness)): #get the numbers of detected hands
            thisHandType=results.multi_handedness[i].classification[0].label #get properties of the detected hand            
            thisHand=results.multi_hand_landmarks[i] #get hand label information
            mpDraw.draw_landmarks(frame, thisHand, mpHands.HAND_CONNECTIONS) #draw tools
            thisHandLMList = []
            for id, lm in enumerate(thisHand.landmark): #id=number,lm=coordinate                 
                thisHandLMList.append([id, lm.x, lm.y,lm.z])
                hx, hy = int(lm.x * w), int(lm.y * h)  #get coordinate of the joint
                cv2.circle(frame, (hx, hy), 5, (255, 0, 0), cv2.FILLED) #make circles with blue color
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

            totalFingers=finger.count(1)
            x1,y1=np.amin(np.array(thisHandLMList)[:,1]),np.amin(np.array(thisHandLMList)[:,2])
            x2,y2=np.amax(np.array(thisHandLMList)[:,1]),np.amax(np.array(thisHandLMList)[:,2])  
            return totalFingers,x1,y1,x2,y2
    else:
        return None,None,None,None,None

def display_game_over(frame, Score):
    game_over_text = "Game Over - Your Score: " + str(Score)
    cv2.putText(frame, game_over_text, (300,300), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    return frame

cap = cv2.VideoCapture(0)

game_start_time = 0 #遊戲尚未開始
game_session = 30 #初始化遊戲設定時間

while cap.isOpened ():  #Is camera open or not
    stime=time.time()
    ret, frame = cap.read() #read camera data
    h, w, c = frame.shape #get resolution(width/height) of the camera
    frame=cv2.flip(frame,1) #flip image：-1:up and down、0: up and down, left and right、1:  left and right

    if game_start_time == 0: #若遊戲尚未開始
        game_start_time = time.time() #取得遊戲開始時的當下時間
    
    current_time = time.time() #取得當下時間
    playing_time = current_time - game_start_time #目前玩了多久
    
    if playing_time >= game_session: #如果目前玩的時間 >= 遊戲設定時間
        Game_Over = display_game_over(frame, Score) #call function
        cv2.imshow('Over', Game_Over)  # Show game over text
        cv2.waitKey(1000)  # wait setting time
        cv2.destroyAllWindows()  # close windows
        break
        
    remain_time = game_session - playing_time #剩餘時間
    remain_time_output = str(int(remain_time)) + "sec" #剩餘時間 output 格式
    cv2.putText(frame, remain_time_output,(300,80), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3 ) #呈現倒數時間，轉成 int 呈現
    
    #Detecting Grasp
    totalFingers,hx1,hy1,hx2,hy2=fist(frame)
    if not (totalFingers==None): #Hand Detected
        if totalFingers<=1: #Fist Clenched
            #Get Palm Area
            #print(hx1,hy1,hx2,hy2)
            if ((x+ObjSizeX//2)>=hx1*w and (x+ObjSizeX//2)<=hx2*w and (y+ObjSizeY//2)>=hy1*h and (y+ObjSizeY//2)<=hy2*h):#If the object is within the palm
                #print("Catched")
                catchObj=True
            else:
                #print("No")
                catchObj=False
        else:
            catchObj=False
    else:
        catchObj=False

 #Basket is in the middle at the bottom
    BucketX=round((w-BucketSizeX)/2)#middle
    BucketY=round(h-BucketSizeY/2-50)#bottom
    frame=addPng(BucketX,BucketY,frame,Bucket)    
 
    if catchObj :#Object Grabbing Process
        #Object follows Palm
        x,y=round(((hx1+hx2)*w-ObjSizeX)//2),round(((hy1+hy2)*h-ObjSizeY)//2)
        frame=addPng(x,y,frame,Obj)
        #Determine if the object is inside the basket----------------------------------------
        if ((x+ObjSizeX//2)>=BucketX and (x+ObjSizeX//2)<=BucketX+BucketSizeX and (y+ObjSizeY//2)>=BucketY and (y+ObjSizeY//2)<=BucketY+BucketSizeY):
            Score=Score+1
            #print("Score=" + str(Score))
            NewObj=True
            catchObj=False
            #playsound.playsound("eat.mp3")

            #Reset Coordinates
            x,y=random.randint(10,w-ObjSizeX-10) ,5
    elif(NewObj==False):#Freefall Process        
        y=y+5
        frame=addPng(x,y,frame,Obj)
    else:#Generate New Object Process
        x,y=random.randint(10,w-ObjSizeX-10) ,5
        NewObj=False  
    etime=time.time()
    fps=round(1/(etime-stime),2)
    cv2.putText(frame, "Get " + str(Score) , (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)    
    cv2.putText(frame, "FPS " + str(fps) , (w-300, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)    
    cv2.imshow('frame', frame)
   
    key=cv2.waitKey(1) #Waiting for User Keyboard Input
    if key==ord('a'):  #'a': capture photo
        cv2.imwrite('webcam.jpg',frame) #save file
    if key==ord('q'):  #'q': quit
        break