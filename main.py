from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title("Photo Mover")

root.geometry("640x1080")

photo = ImageTk.PhotoImage(Image.open("./images/1(1).jpg"))
label2 = Label(root, image=photo)
label2.pack()
#root.resizable(False, False)

root.mainloop()