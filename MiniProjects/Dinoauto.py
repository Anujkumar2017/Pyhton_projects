import pyautogui 
from PIL import Image,ImageGrab
import time

def isCollide(data):
    # dectect for cactus
    for i in range(250,320):
        for j in range(380,460):
            if 50<data[i,j]<100 :
                pyautogui.keyDown('up')
                return True
    
    # dectect for bird
    for i in range(220,250):
        for j in range(210,380):
            if data[i,j]<100:
                pyautogui.keyDown('down')
                return True




if __name__=="__main__":
    time.sleep(3)
    pyautogui.press('space')
    # time.sleep(2)
    # pyautogui.press('up')
    while True:
        image =ImageGrab.grab().convert('L')
        data=image.load()
        if isCollide(data):
            print("detected")
        # for i in range(260,300):
        #     for j in range(380,460):
        #         data[i,j]=0
        
        # for i in range(220,260):
        #     for j in range(210,380):
        #         data[i,j]=180
        # image.show()
