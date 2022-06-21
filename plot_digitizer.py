# importing the module
import cv2
import tkinter as tk
from tkinter.filedialog import askopenfilename
import csv


#build and destroy tkinter just to get dialog box
root= tk.Tk()
root.withdraw()

red =[0,0,255]
# function to display the coordinates of
# of the points clicked on the image


dataPoints=[]
count=0
refx=[]
refy=[]
origin_x=[]
origin_y=[]

def click_event(event, x, y, flags, params):
    global count,dataPoints,origin_x,origin_y,refx,refy
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        if count == 0:
            origin_x.extend((x,float(input("What is the x value of the origin?"))))
            origin_y.extend((y,float(input("What is the y value of the origin?"))))
            print("choose a point on the x axis")
            color=(0,255,0)
            
        elif count == 1:
            refx.extend((x,float(input("What is the x value of the point selected?"))))
            print("choose a point on the y axis")
            color=(0,255,0) 
        elif count == 2:
            refy.extend((y,float(input("What is the y value of the point selected?"))))
            print("Choose datapoints")
            color=(0,255,0)
        else:
            # displaying the coordinates
            # on the Shell
            color=(255,0,0)
            x_val=(refx[1]-origin_x[1])/(refx[0]-origin_x[0])*(x-origin_x[0])+origin_x[1]
            y_val=(refy[1]-origin_y[1])/(refy[0]-origin_y[0])*(y-origin_y[0])+origin_y[1]
            dataPoints.append([x_val,y_val])
            font = cv2.FONT_HERSHEY_SIMPLEX
            print(x_val,y_val)
            cv2.putText(img_s,str(round(x_val,1))+ '+' + str(round(y_val,1)), (x+10,y), font,
                    .5, color, 2)
        cv2.circle(img_s,(x,y),5,color,2)

        cv2.imshow('Plot', img_s)
            
        count+=1
 
# driver function
if __name__=="__main__":
 
    # reading the image
    file_path = askopenfilename()
    img = cv2.imread(file_path, 1)

    #resizing to get in window
    img_s=cv2.resize(img,(960,640))
    cv2.imshow('Plot', img_s)

    
    print("Choose an origin (treated as 0,0)")
    #start looking forclicks
    cv2.setMouseCallback('Plot', click_event)
    
    # wait for a key to be pressed to exit
    cv2.waitKey(0)

    with open('Data.csv', 'w', newline ='') as f:
      
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerows(dataPoints)

    cv2.destroyAllWindows()

