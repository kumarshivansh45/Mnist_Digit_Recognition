# IMPORTING MODULES AND DIRECTORIES
import tkinter as tk
import copy
from tkinter import *
from PIL import ImageGrab , Image , ImageDraw
from tkinter.font import Font
import os
import numpy as np
import pathlib
import matplotlib.pyplot as plt


# FUNCTIONS AT THE TOP (AFTER IMPORTS , OBVIOUSLY)
def train():
    print("training the model ...")
    def get_mnist():
        with np.load(f"./testing/mnist.npz") as f:
            images, labels = f["x_train"], f["y_train"]
        images = images.astype("float32") / 255
        images = np.reshape(images, (images.shape[0], images.shape[1] * images.shape[2]))
        labels = np.eye(10)[labels]
        return images, labels
    """
    w = weights, b = bias, i = input, h = hidden, o = output, l = label
    e.g. w_i_h = weights from input layer to hidden layer
    """
    images, labels = get_mnist()
    global w_1_2,w_2_3,w_3_4,w_4_5,b_1_2,b_2_3,b_3_4,b_4_5
    w_1_2 = np.random.uniform(-0.5, 0.5, (100, 784))
    w_2_3 = np.random.uniform(-0.5,0.5,(50,100))
    w_3_4 = np.random.uniform(-0.5,0.5,(20,50))
    w_4_5 = np.random.uniform(-0.5, 0.5, (10, 20))
    b_1_2 = np.zeros((100, 1))
    b_2_3 = np.zeros((50, 1))
    b_3_4 = np.zeros((20,1))
    b_4_5 = np.zeros((10,1))
    learn_rate = 0.01
    nr_correct = 0
    epochs = 3
    for epoch in range(epochs):
        for img, l in zip(images, labels):
            img.shape += (1,)
            l.shape += (1,)
            # Forward propagation input -> hidden
            h_2 = b_1_2 + w_1_2 @ img
            h_2 = 1 / (1 + np.exp(-h_2))
            h_3 = b_2_3 + w_2_3 @ h_2
            h_3 = 1/(1 + np.exp(-h_3))
            h_4 = b_3_4 + w_3_4 @ h_3
            h_4 = 1/(1+ np.exp(-h_4))
            h_5 = b_4_5 + w_4_5 @ h_4
            h_5 = 1/(1 + np.exp(-h_5))
    #         Forward propagation hidden -> output
    #         o_pre = b_h_o + w_h_o @ h
    #         o = 1 / (1 + np.exp(-o_pre))
            # Cost / Error calculation
            e = 1 / len(h_5) * np.sum((h_5 - l) ** 2, axis=0)
            nr_correct += int(np.argmax(h_5) == np.argmax(l))
            # Backpropagation output -> hidden (cost function derivative)
            delta_h_5 = h_5 - l
            w_4_5 += -learn_rate * delta_h_5 @ np.transpose(h_4)
            b_4_5 += -learn_rate * delta_h_5
            # Backpropagation hidden -> input (activation function derivative)
            delta_h_4 = np.transpose(w_4_5) @ delta_h_5 * (h_4 * (1 - h_4))
            w_3_4 += -learn_rate * delta_h_4 @ np.transpose(h_3)
            b_3_4 += -learn_rate * delta_h_4
            delta_h_3 = np.transpose(w_3_4) @ delta_h_4 * (h_3 * (1 - h_3))
            w_2_3 += - learn_rate * delta_h_3 @ np.transpose(h_2)
            b_2_3 += -learn_rate * delta_h_3
            delta_h_2 = np.transpose(w_2_3) @ delta_h_3 * (h_2 * (1 - h_2))
            w_1_2 += -learn_rate * delta_h_2 @ np.transpose(img)
            b_1_2 += -learn_rate * delta_h_2
        # Show accuracy for this epoch
        print(f"Acc: {round((nr_correct / images.shape[0]) * 100, 2)}%")
        nr_correct = 0

def predict():
    global w_1_2,w_2_3,w_3_4,w_4_5,b_1_2,b_2_3,b_3_4,b_4_5
    from PIL import Image
    image22 = Image.open("./images/yay.png")
    im1 = image22.resize((28,28))
    im1.save('./images/WOW.png')
    im2 = Image.open("./images/WOW.png",'r')
    im3 = im2.convert('L')
    im3.save('./images/test_gray.png')
    img = np.array(list(im3.getdata()))
    def trans(z):
        return(-1*(z-255))
    img = trans(img)
    img = np.reshape(img,(784,1))
    plt.imshow(img.reshape(28, 28), cmap="Greys")
    # plt.show()
    # Forward propagation input -> hidden
    h_2 = b_1_2 + w_1_2 @ img
    h_2 = 1 / (1 + np.exp(-h_2))
    h_3 = b_2_3 + w_2_3 @ h_2
    h_3 = 1/(1 + np.exp(-h_3))
    h_4 = b_3_4 + w_3_4 @ h_3
    h_4 = 1/(1+ np.exp(-h_4))
    h_5 = b_4_5 + w_4_5 @ h_4
    h_5 = 1/(1 + np.exp(-h_5))
    print(f"success if its a {h_5.argmax()} :)")



def pil_image():
    #drawing parallely on another PIL image
    global image1, drawImg , img_black , img_white
    img_width = 370
    img_height = 370
    img_center = img_height//2
    img_white = (255, 255, 255)
    img_black = (0,0,0)
    # PIL create an empty image and draw object to draw on
    # memory only, not visible
    image1 = Image.new("RGB", (img_width, img_height), img_white)
    drawImg = ImageDraw.Draw(image1)

def save_image(event):
    print("saved")
    destination = "./images/yay.png"
    # xx = window.winfo_rootx() + canvas1.winfo_x()
    # yy = window.winfo_rooty() + canvas1.winfo_y()
    # xx1 = xx + window.winfo_width()
    # yy1 = yy + window.winfo_height()
    # ImageGrab.grab(bbox=(xx, yy, xx1, yy1)).save(destination)
    image1.save(destination)

# def ppt(event):
#     print(event.x,event.y)

def motion(event):
    global last_x , last_y
    last_x,last_y = event.x, event.y
    # print('{}, {}'.format(last_x, last_y))

def hit_enter(event):
    print("pressed enter")

def erase(event):
    canvas1.delete('all')
    pil_image()

def draw(event):
    def circle(draw, center, radius, fill):
        drawImg.ellipse(
            (center[0] - radius + 1, center[1] - radius + 1, center[0] + radius - 1, center[1] + radius - 1),
            fill=fill, outline=None)
    global last_x,last_y,drawImg
    cpy_x = copy.deepcopy(event.x)
    cpy_y = copy.deepcopy(event.y)
    WIDTH = 35
    canvas1.create_line((last_x, last_y, cpy_x, cpy_y), fill="black", width=WIDTH,smooth= True ,capstyle = tk.ROUND)
    drawImg.line([last_x, last_y, cpy_x, cpy_y], fill=img_black ,width=20)
    circle(drawImg, (last_x, last_y), WIDTH / 2, img_black)
    circle(drawImg, (cpy_x, cpy_y), WIDTH / 2, img_black)
    last_x , last_y = event.x , event.y


global w_1_2,w_2_3,w_3_4,w_4_5,b_1_2,b_2_3,b_3_4,b_4_5
# train()
window = Tk() # creating the main window
window.resizable(False, False) # disabling window size resizing
# defining window geometry
window.geometry("600x400")
# giving icon and title to the window
window.title("MNIST digit recognition")
photo = PhotoImage(file = "./icon.png")
window.iconphoto(False, photo)
window.configure(bg='white') # setting white color to the window




# TKINTER WIDGETS

canvas1 = Canvas(window,bg="#FAEAC5",bd=2, width=370, height=370, relief="ridge",cursor = "x_cursor")
# canvas1.grid(column=500)
canvas1.pack(side = "left",anchor="s")
frame1 = Frame(window, highlightbackground="black",highlightthickness=1,width=230, height=370, bd= 0)
frame1.pack(side = "right",anchor = "s",padx=4,pady=4)
canvas2 = Canvas(frame1, bg='white', width=230, height=370)
# canvas2.create_text(109, 30, text="""Draw any digit from 0-9 on the canvas \npress <ENTER> to predict\npress <BACKSPACE> to clear screen\n===================================""", fill="black", font=('Helvetica 8 bold'))
# canvas2.create_text(80, 70, text=f"{predict()}", fill="red", font=('Helvetica 8 bold'))

canvas2.pack()
# l = Label(window, text="Fact of the Day")
# l.config(font=("Courier", 10))
# l.pack()



pil_image() # for creating an invisible white PIL image in parallel

canvas1.bind('<Motion>', motion)
window.bind('<Return>',save_image)
canvas1.bind('<B1-Motion>',draw)
window.bind('<BackSpace>',erase)

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window.mainloop()
img = Image.open("./images/yay.png")
# img.show()














