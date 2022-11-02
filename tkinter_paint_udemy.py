# IMPORT STATEMENTS
from tkinter import * #----------------------
from PIL import Image, ImageDraw, ImageTk, ImageGrab
import PIL
from tkinter import colorchooser
import tkinter.ttk as ttk  # now what the fuck is a ttk
from tkinter import filedialog
from tkinter import messagebox

root = Tk() # MAIN WINDOW ELEMENT
root.title('Paint!') # TITLE OF THE WINDOW
root.geometry('800x800') # SIZE OF THE WINDOW

def pil_image():
# DIMENTIONS TO KEEP THE IMAGE AT THE CENTRE OF THE SCREEN
w = 600
h = 400
x = w/2
y = h/2
# CREATING THE IMAGE ELEMENT
white = (250,234,197)
image1 = PIL.Image.new('RGB', (w, h), white)
# draw = ImageDraw.Draw(image1)

# CREATING AND PACKING THE CANVAS
my_canvas = Canvas(root, width=w, height=h, bg='#ffffff')
my_canvas.pack(pady=20) # WHAT IS "PADY" , I DONT KNOW ...

# Default colors of brush and canvas
brush_color = 'black'
bg_color = 'white'


def paint(e): # DEFINING A FUNCTION , LETS FIND OUT WHAT IS e
    # Brush parameters
    brush_width = '%0.0f' % float(my_slider.get()) # '%0.0f is used to add trailing zeroes'
    print(my_slider.get())
    print(brush_width)
    # Brush Types/Cap Styles: BUTT, ROUND, PROJECTING
    brush_type2 = brush_type.get() # selecting the brush type from the bullets
    # Starting position
    x1 = e.x - 1 # find out whats 'e,x,y'
    y1 = e.y - 1
    # Ending position
    x2 = e.x + 1
    y2 = e.y + 1
    # Draw on the canvas
    my_canvas.create_line(x1, y1, x2, y2, fill=brush_color, width=brush_width, capstyle=brush_type2, smooth=True)
    old_x = e.x
    old_y = e.y


def reset(event):
    old_x = None
    old_y = None


def save_as_png():
    result = filedialog.asksaveasfilename(initialdir='/Users/johfa/Pictures/Paintings', filetypes=(('png files', '*.png'), ('all files', '*.*')))
    if result.endswith('.png'):
        pass
    else:
        result = result + '.png'
    # result_label = Label(root, text=result)
    # result_label.pack(pady=20)
    if result:
        x=root.winfo_rootx()+my_canvas.winfo_x()
        y=root.winfo_rooty()+my_canvas.winfo_y()
        x1=x+my_canvas.winfo_width()
        y1=y+my_canvas.winfo_height()
        ImageGrab.grab().crop((x,y,x1,y1)).save(result)

        messagebox.showinfo('Image Saved', 'Your Image Has Been Saved!')


my_canvas.bind('<B1-Motion>', paint)


def clear_screen():
    my_canvas.delete(ALL)
    my_canvas.config(bg='white')


def change_brush_color():
    global brush_color
    brush_color = 'black'
    brush_color = colorchooser.askcolor(color=brush_color)[1]
    # color = Label(root, text=brush_color)
    # color.pack(pady=20)


def change_canvas_color():
    global bg_color
    bg_color = 'white'
    bg_color = colorchooser.askcolor(color=bg_color)[1]
    my_canvas.config(bg=bg_color)


def change_brush_size(command_thing):
    slider_label.config(text='%0.0f' % float(my_slider.get()))



# Create brush options frame
brush_options_frame = Frame(root)
brush_options_frame.pack(pady=20)

# Brush size
brush_size_frame = LabelFrame(brush_options_frame, text='Brush Size')
brush_size_frame.grid(row=0, column=0, padx=50)
# Brush slider
my_slider = ttk.Scale(brush_size_frame, from_=1, to=100, command=change_brush_size, orient=VERTICAL, value=10)
my_slider.pack(pady=10, padx=10)
# Brush slider label
slider_label = Label(brush_size_frame, text=my_slider.get())
slider_label.pack(pady=5)


# Brush type
brush_type_frame = LabelFrame(brush_options_frame, text='Brush Type', height=400)
brush_type_frame.grid(row=0, column=1, padx=50)
# Create string variable for brush type to set and get
brush_type = StringVar()
brush_type.set('round')
# Create radio buttons for brush type
brush_type_radio1 = Radiobutton(brush_type_frame, text='Round', variable=brush_type, value='round')
brush_type_radio2 = Radiobutton(brush_type_frame, text='Slash', variable=brush_type, value='butt')
brush_type_radio3 = Radiobutton(brush_type_frame, text='Diamond', variable=brush_type, value='projecting')
# Put the radio buttons on the screen
brush_type_radio1.pack(anchor=W)
brush_type_radio2.pack(anchor=W)
brush_type_radio3.pack(anchor=W)


# Change color
change_colors_frame = LabelFrame(brush_options_frame, text='Change Color')
change_colors_frame.grid(row=0, column=2)
# Change brush color button
brush_color_button = Button(change_colors_frame, text='Brush Color', command=change_brush_color)
brush_color_button.pack(pady=10, padx=10)
# Change canvas color button
canvas_color_button = Button(change_colors_frame, text='Canvas Color', command=change_canvas_color)
canvas_color_button.pack(pady=10, padx=10)


# The program options frame
options_frame = LabelFrame(brush_options_frame, text='Options')
options_frame.grid(row=0, column=3, padx=50)

# Create clear button
clear_btn = Button(options_frame, text='Clear Screen', command=clear_screen)
clear_btn.pack(padx=10, pady=10)
# Create save image button
save_image_btn = Button(options_frame, text='Save as PNG', command=save_as_png)
save_image_btn.pack(pady=10, padx=10) #save image button

root.mainloop() # mainloop