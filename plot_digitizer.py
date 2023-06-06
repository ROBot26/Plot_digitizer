# importing the module
import cv2
import tkinter as tk
import numpy as np
from tkinter.filedialog import askopenfilename, asksaveasfile
import csv


#build and destroy tkinter just to get dialog box
root= tk.Tk()
root.withdraw()

red =[0,0,255]
# function to display the coordinates of
# of the points clicked on the image


dataPoints=[]
count=0
x_pix_scale=[]
x_num_scale=[]
y_pix_scale=[]
y_num_scale=[]
x_flag=0
y_flag=0


def check_null_str(input_str):
    if input_str == '' or input_str is None:
        print('No file input given!')
        exit()

def click_event(event, x, y, flags, params):
    global count,dataPoints,x_pix_scale,x_num_scale,y_num_scale,y_pix_scale,y_flag,x_flag
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        if count == 0:
            x_pix_scale.append(float(x))
            x_num_scale.append(float(input("What is the x value of the origin?")))
            y_pix_scale.append(float(y))
            y_num_scale.append(float(input("What is the y value of the origin?")))
            print("choose a point on the x axis")
            color=(0,255,0)
            
        elif count == 1:
            x_pix_scale.append(float(x))
            x_num_scale.append(float(input("What is the x value of the point selected?")))
            x_flag=float(input("Is the X axis linear or logarithmic (0/1)?"))
            if x_flag:
                x_num_scale=np.log10(x_num_scale)
            print("choose a point on the y axis")
            color=(0,255,0) 
        elif count == 2:
            y_pix_scale.append(float(y))
            y_num_scale.append(float(input("What is the y value of the point selected?")))
            y_flag = float(input("Is the Y axis linear or logarithmic (0/1)?"))
            if y_flag:
                y_num_scale=np.log10(y_num_scale)
            print("Choose datapoints")
            color=(0,255,0)
        else:
            # displaying the coordinates
            # on the Shell
            color=(255,0,0)

            x_val =(x_num_scale[1]-x_num_scale[0])/(x_pix_scale[1]-x_pix_scale[0])*(x-x_pix_scale[0])+x_num_scale[0]
            y_val =(y_num_scale[1] - y_num_scale[0]) / (y_pix_scale[1] - y_pix_scale[0]) *(y-y_pix_scale[0]) + y_num_scale[0]
            if x_flag:
                x_val = 10**x_val
            if y_flag:
                y_val = 10**y_val

            dataPoints.append([x_val,y_val])
            font = cv2.FONT_HERSHEY_SIMPLEX
            print(x_val,y_val)
            cv2.putText(img_s,str(round(x_val,1)) + ',' + str(round(y_val,1)), (x+10,y), font,
                    .5, color, 2)
        cv2.circle(img_s,(x,y),5,color,2)

        cv2.imshow('Plot', img_s)
            
        count+=1
 
# driver function
if __name__=="__main__":
 
    # reading the image
    file_path = askopenfilename()
    print(file_path)
    check_null_str(file_path)
    img = cv2.imread(file_path, 1)

    #resizing to get in window
    img_s=cv2.resize(img,(960,640))
    cv2.imshow('Plot', img_s)

    
    print("Choose an origin (treated as 0,0)")
    #start looking forclicks
    cv2.setMouseCallback('Plot', click_event)
    
    # wait for a key to be pressed to exit
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    save_file_path = asksaveasfile()
    check_null_str(save_file_path)

    with open(save_file_path, 'w', newline ='') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerows(dataPoints)



