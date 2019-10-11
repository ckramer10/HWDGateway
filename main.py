from Tkinter import *
from PIL import ImageTk, Image
from threading import Thread
import RPi.GPIO as GPIO
import time
import socket

 #Initialize variables
blackPath = "./black.jpg"
count = 0
picture = None
win = None
bool = True


#Shows image for indicated amount of time in ms
def showPicture():
    global count, picture
    path = str(count) + ".jpg"
    im = Image.open(path)
    picture.image = ImageTk.PhotoImage(im)
    picture.create_image(0,0,anchor="nw",image=picture.image)


#Displays black screen
def hidePicture():
    global blackPath, picture
    im = Image.open(blackPath)
    picture.image = ImageTk.PhotoImage(im)
    picture.create_image(0,0,image=picture.image, anchor="nw")


#Resets image display order
def reset():
    global count
    count = 0

def exitProgram():
    global win
    win.quit()

def checkButton():
     global count, bool
     while bool == True:
         input_state = GPIO.input(18)
         if input_state == False:
             input_state = GPIO.input(18)
             while input_state == False:
             	input_state = GPIO.input(18)
             print('Button Pressed')
             count+= 1
             if count == 5:
                count = 0
             sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
             sock.connect((host,port))
             sock.send(b'1')
	         sock.close()
             
#Check Photoresistor for light
def checkLight():
    global win
    lum = RCtime(23)
    if (lum < 500):
	showPicture()
    else:
	hidePicture()
    win.after(100, checkLight)

#Calculate light intensity
def RCtime (RCpin):
    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(RCpin, GPIO.IN)
    while (GPIO.input(RCpin) == GPIO.LOW):
	reading += 1

    return reading

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    host = '192.168.2.4'
    port = 2041
    global win

    #Initialize windows
    win = Tk()
    win.title("CS 4605 Demo")
    win.geometry("1200x800")
    win["bg"] = "black"

    global blackPath
    global picture


    #title
    title = Label(win,text = "CS 4605 HWD Demo",font=(None, 25), width = 50, height = 4,borderwidth = 0, highlightthickness = 0, foreground="white")
    title.place(relx=.5, rely=.07, anchor="center")
    title["bg"] = "black"

    #image
    picture = Canvas(win, width=640, height=360,borderwidth = 0, highlightthickness = 0)
    picture.place(relx=.5, rely=.5, anchor="center")
    im = Image.open(blackPath)
    picture.image = ImageTk.PhotoImage(im)
    picture.create_image(600,400,anchor=CENTER,image=picture.image)


    #exit button
    exitButton = Button(win, text='Exit Program', command=exitProgram, height=1, width=20)
    exitButton.place(relx=.75, rely=.95, anchor="center")


    #reset button
    resetButton = Button(win, text='Reset', command=reset, height=1, width=20)
    resetButton.place(relx=.25, rely=.95, anchor="center")


    win.after(1, checkLight)
    win.mainloop()


if __name__ == '__main__':
    mainThread = Thread(target = main, args = [])
    buttonThread = Thread(target = checkButton, args = [])
    mainThread.start()
    buttonThread.start()
    mainThread.join()
    bool = False
    buttonThread.join()
