import tkinter
import cv2
from PIL import Image,ImageTk 
from functools import partial
import threading
import imutils
import time


#Width and height of main window
SET_WIDTH = 700
SET_HEIGHT = 400
flag =True
stream = cv2.VideoCapture('clips\clip.mp4')
def play(speed):
    global flag
    print(f"You clicked on play.Speed is {speed}")
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES,frame1+speed)

    grabbed, frame =stream.read()
    frame =cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width = SET_WIDTH, height=SET_HEIGHT)
    frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
    canvas.image=frame
    canvas.create_image(0,0,anchor=tkinter.NW,image=frame)
    if flag:
        canvas.create_text(150,20,fill='black',font='Times 26 bold',text = 'Decision Pending')
    flag = not flag

def pending(decision):
    #1.Display decision pending image
    frame = cv2.cvtColor(cv2.imread("Images\Decision_pending.png"),cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width = SET_WIDTH, height=SET_HEIGHT)
    frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
    canvas.image=frame
    canvas.create_image(0,0,anchor=tkinter.NW,image=frame)
    #2.wait for 1 sec
    time.sleep(1)
    #3.Display sponsor image
    frame = cv2.cvtColor(cv2.imread("Images\Sponsor.png"),cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width = SET_WIDTH, height=SET_HEIGHT)
    frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
    canvas.image=frame
    canvas.create_image(0,0,anchor=tkinter.NW,image=frame)
    canvas.pack()
    #4.wait for 1.5 sec
    time.sleep(1.5)
    #5.display out/not_out image
    if decision =='not_out':
        decisionImg ='Images\\notout.png'
    else:
        decisionImg ='Images\out.png' 
    frame = cv2.cvtColor(cv2.imread(decisionImg),cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width = SET_WIDTH, height=SET_HEIGHT)
    frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
    canvas.image=frame
    canvas.create_image(0,0,anchor=tkinter.NW,image=frame)

def out():
    thread = threading.Thread(target=pending,args=("out",))
    thread.deamon =1
    thread.start()
    print("dicision is Out!")
    
def not_out():
    thread = threading.Thread(target=pending,args=("not_out",))
    thread.deamon =1
    thread.start()
    print('decision is Not Out!')


#Tkinter gui starts here
window = tkinter.Tk()
window.title("Third Umpire Window")
cv_img= cv2.cvtColor(cv2.imread("Images\Welcome.png"),cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width= SET_WIDTH, height=SET_HEIGHT)
photo = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
canvas.create_image(0, 0, anchor=tkinter.NW, image=photo)
canvas.pack()

#setting up buttons 
btn1 = tkinter.Button(window,text="<< Previous(fast)" ,width = 20,fg='green',activebackground="blue",bd =4,command=partial(play,-15))
btn1.pack()
btn2 = tkinter.Button(window,text="Next(fast) >>" ,width = 20,fg='green',activebackground="blue",bd =4,command=partial(play,15))
btn2.pack()
btn3 = tkinter.Button(window,text="<< Previous(Slow)" ,width = 20,fg='green',activebackground="blue",bd =4,command=partial(play,-2))
btn3.pack()
btn4 = tkinter.Button(window,text="Next(Slow) >>" ,width =20 ,fg='green',activebackground="blue",bd =4,command=partial(play,2))
btn4.pack()
btn5 = tkinter.Button(window,text="Give Not Out" ,width =20 ,fg='green',activebackground="blue",bd =4,command=not_out)
btn5.pack()
btn6 = tkinter.Button(window,text="Give Out" ,width =20 ,fg='green',activebackground="blue",bd =4,command=out)
btn6.pack()

window.mainloop()

