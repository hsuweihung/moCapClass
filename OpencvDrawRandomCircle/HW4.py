import random
from PIL import Image
import cv2
from IPython.display import display

image4 = cv2.imread('sakura.jpg')
image4 = cv2.cvtColor(image4, cv2.COLOR_BGR2RGB) # Converting BGR to RGB
h, w = image4.shape[:2] # Extracting the height and width of an image
num_circles = random.randint(400, 500) #產生隨機白點

for i in range(num_circles): #要產生的隨機白點中，指定隨機 x,y 位置
    x = random.randint(0, w)
    y = random.randint(0, h)
    cv2.circle(image4, center=(x, y), radius=5, color=(255, 255, 255), thickness=-1)

display(Image.fromarray(image4))
