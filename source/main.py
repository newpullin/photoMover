import shutil
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
nowStatus = StringVar()
skipNum = StringVar()

#now_process는 인덱스 보다 1 증가된 값
now_process = 0
total_process = 0
prev_result = ""
files = None


shortcut_dict = {}

root.geometry("840x1000")

left_frame = Frame(root)
left_frame.grid(row=0, column=0)

#사진
photo = ImageTk.PhotoImage(Image.open("../assets/cat.jpg").resize((670, 480)))
photo_label = Label(left_frame, image=photo)
photo_label.pack()

#이동결정

moveChkBox = Checkbutton(left_frame, text="원본을 이동 시킬까요?", variable=moveChkVar)
moveChkBox.deselect()
moveChkBox.pack()
print(moveChkVar.get())
#폴더 설정
folderSetFrame = LabelFrame(left_frame, text="폴더 설정", pady=10)
folderSetFrame.pack()

processFrame = LabelFrame(left_frame, text="진행상태", pady=10)
processFrame.pack()
nowStatus.set(f"현재 {now_process}/{total_process} 이전 결과: {prev_result}")

def skip():
    global now_process
    global skipNum
    global nowStatus
    global prev_result
    global total_process

    now_process = int(skipNum.get())
    nowStatus.set(f"현재 {now_process}/{total_process} 이전 결과: {prev_result}")


Label(processFrame, textvariable=nowStatus).grid(row=0, column=0)
Entry(processFrame, textvariable=skipNum, width=5).grid(row=1, column=0)
Button(processFrame, text="스킵", command=skip).grid(row=1, column=1)

target_folder.set('대상폴더: c:/')
save_folder.set('저장폴더: c:/')


def set_folder(changed_path, refresh=False):
    global files
    global total_process
    global now_process
    folder_path = filedialog.askdirectory(title="폴더를 정하십시오")
    if not os.path.isdir(folder_path):
        changed_path.set('c:/')
    else:
        changed_path.set(folder_path)
        if refresh:
            files = os.listdir(folder_path)
            total_process = len(files)
            now_process = 1
            nowStatus.set(f"현재 {now_process}/{total_process} 이전 결과: ")
            now_file = files[0]
            image = Image.open(target_folder.get() + "/" + now_file)

            new_width = int(image.width*image.height/480) if image.height < 480 else int(image.width*480/image.height)

            photo = ImageTk.PhotoImage(image.resize((new_width, 480)))
            photo_label.configure(image=photo)
            photo_label.image = photo


Label(folderSetFrame, text="목표폴더 :").grid(row=0, column=0, padx=10)
Label(folderSetFrame, textvariable=target_folder).grid(row=0, column=1, padx=10)
Button(folderSetFrame, text="변경", command=lambda: set_folder(target_folder, True)).grid(row=0, column=2, padx=10)
Label(folderSetFrame, text="저장폴더 :").grid(row=1, column=0, padx=10)
Label(folderSetFrame, textvariable=save_folder).grid(row=1, column=1, padx=10)
Button(folderSetFrame, text="변경", command=lambda: set_folder(save_folder)).grid(row=1, column=2, padx=10)


# 우측 리스트 관리
list_frame = Frame(root)
list_frame.grid(row=0, column=1)

def addShortCut():
    key = shortcutKey.get()
    name = shortcutName.get()

    if len(key) != 1 or len(name) == 0:
        return False

    list_file.insert(END, name + " : " + key)
    shortcut_dict[key] = name



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

def key(event):
    global prev_result
    global now_process
    global photo_label
    pushed = event.char
    if pushed in shortcut_dict.keys():
        if moveChkVar.get() == 0:
            folder_path = save_folder.get() + "/" + shortcut_dict[pushed]
            if not os.path.isdir(folder_path):
                os.makedirs(folder_path)

            now_file = files[now_process-1]
            shutil.copy(target_folder.get() + "/" + now_file, folder_path + "/" + now_file)
            prev_result = shortcut_dict[pushed]
            if now_process-1 < len(files):
                now_process += 1
            now_file = files[now_process - 1]
            #사진 갱신
            photo = ImageTk.PhotoImage(Image.open(target_folder.get() + "/" + now_file).resize((670, 480)))
            photo_label.configure(image=photo)
            photo_label.image = photo
            nowStatus.set(f"현재 {now_process}/{total_process} 이전 결과: {prev_result}")
            # copy 하라
        else :
            pass
            #이동시켜라
        print(shortcut_dict[pushed])


event_input = Entry(left_frame)
event_input.pack()
event_input.bind("<Key>", key)


root.mainloop()

def imageWidthFixedHeight(photo, fixHeight):
    pass

class PhotoMover:
    def __init__(self, title="Photo classifier", window_size="840x1000", FIXED_HEIGHT=480):
        # TK root frame
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(window_size)
        # CONSTANCE
        self.FIXED_HEIGHT = FIXED_HEIGHT

        # Tk variable
        self.target_folder = StringVar()
        self.save_folder = StringVar()
        self.moveChkVar = IntVar()
        self.shortcutName = StringVar()
        self.shortcutKey = StringVar()
        self.nowStatus = StringVar()
        self.skipNum = StringVar()

        # normal variable
        self.now_process = 0
        self.total_process = 0
        self.prev_result = ""
        self.files = None
        self.shortcut_dict = {}

        # component of program
        self.left_frame = Frame(self.root)

    def construct_layout(self):
        pass

    def start(self):
        pass

"""
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
print(moveChkVar.get())
#폴더 설정
folderSetFrame = LabelFrame(left_frame, text="폴더 설정", pady=10)
folderSetFrame.pack()

processFrame = LabelFrame(left_frame, text="진행상태", pady=10)
processFrame.pack()
nowStatus.set(f"현재 {now_process}/{total_process} 이전 결과: {prev_result}")

"""
class LeftFrame:
    def __init__(self):
        self.left_frame = Frame(root)
        self.left_frame.grid(row=0, column=0)

        self.photo = None
        self.photo_label = None
        self.moveChkBox = None
        folderSetFrame = None

        processFrame = None



    def construct(self, root):
        self.left_frame = Frame(root)
        self.left_frame.grid(row=0, column=0)

