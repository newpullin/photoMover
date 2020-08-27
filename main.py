from tkinter import *
from PIL import Image, ImageTk
import os
import tkinter.ttk as ttk
from tkinter import filedialog

root = Tk()
root.title("Photo classifier")

target_folder = StringVar()
save_folder = StringVar()
moveChkVar = IntVar()
shortcutName = StringVar()
shortcutKey = StringVar()

root.geometry("840x1000")

left_frame = Frame(root)
left_frame.grid(row=0, column=0)

#사진
photo = ImageTk.PhotoImage(Image.open("./assets/cat.jpg").resize((670, 480)))
photo_label = Label(left_frame, image=photo)
photo_label.pack()

#이동결정

moveChkBox = Checkbutton(left_frame, text="원본을 이동 시킬까요?", variable=moveChkVar)
moveChkBox.deselect()
moveChkBox.pack()

#폴더 설정
folderSetFrame = LabelFrame(left_frame, text="폴더 설정", pady=10)
folderSetFrame.pack()

target_folder.set('대상폴더: c:/')
save_folder.set('저장폴더: c:/')


def set_folder(changed_path, add_text=""):
    folder_path = filedialog.askdirectory(title="목표 폴더를 정하십시오")
    if not os.path.isdir(folder_path):
        changed_path.set('c:/')
    else:
        changed_path.set(add_text + folder_path)



Label(folderSetFrame, textvariable=target_folder).grid(row=0, column=0, padx=10)
Button(folderSetFrame, text="변경", command=lambda: set_folder(target_folder,"대상폴더: ")).grid(row=0, column=1, padx=10)
Label(folderSetFrame, textvariable=save_folder).grid(row=1, column=0, padx=10)
Button(folderSetFrame, text="변경", command=lambda: set_folder(save_folder,"저장폴더: ")).grid(row=1, column=1, padx=10)


# 우측 리스트 관리
list_frame = Frame(root)
list_frame.grid(row=0, column=1)

def addShortCut():
    key = shortcutKey.get()
    name = shortcutName.get()

    if len(key) != 1 or len(name) == 0:
        return False

    list_file.insert(END, name + " : " + key)



listAddFrame = LabelFrame(list_frame, text="단축키설정", width=50)
listAddFrame.grid(row=0, column=0)
Label(listAddFrame, text="폴더이름").grid(row=0, column=0)
Entry(listAddFrame, width=10, textvariable=shortcutName).grid(row=0, column=1)
Label(listAddFrame, text="단축키").grid(row=1, column=0)
Entry(listAddFrame, width=10, textvariable=shortcutKey).grid(row=1, column=1)
Button(listAddFrame, text="추가", command=addShortCut).grid(row=1, column=2)


list_file = Listbox(list_frame, selectmode="extended", height=20)
list_file.grid(row=1, column=0)

Button(list_frame, text="삭제").grid(row=2, column=0)
Button(list_frame, text="옵션저장").grid(row=3, column=0)
Button(list_frame, text="옵션가져오기").grid(row=4, column=0)
root.mainloop()
