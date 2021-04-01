from tkinter import *
from tkinter import ttk
from tkinter.font import Font
import threading

import sys
sys.path.append('..')
import macro 

import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle
    
    
root = Tk()
root.geometry("1200x700")
content_top = ttk.Frame(root)

# --! Custom Text Widget
class ScrollText(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        frame_ = ttk.Frame(content_top, borderwidth=5, relief="flat", width=380, height=135)

        tk.Frame.__init__(self, *args, **kwargs)
        self.text = Text(frame_, wrap=WORD, width=55, height= 16.2,bg='#2b2b2b',foreground="#d1dce8", insertbackground='white',selectbackground="blue")

        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.numberLines = TextLineNumbers(frame_, width=40, height=324,bg='#313335')
        self.numberLines.attach(self.text)

        file_label_image = PhotoImage(file="./icons/macro_list2.png")
        file_label = Label(frame_, text="File",image=file_label_image,compound="left")
        file_label.image = file_label_image
        save_btn_icon = PhotoImage(file="./icons/icons8-save-50.png")
        save_btn = Button(frame_ , text = "Save",image=save_btn_icon,compound="top", relief="flat")
        save_btn.image = save_btn_icon
        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numberLines.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.text.bind("<MouseWheel>", self.onPressDelay)
        frame_.grid(column=4, row=6, columnspan=3, rowspan=8,padx=40)
        self.numberLines.grid(column=0, row=1,rowspan=3)
        self.text.grid(column=1, row=2,columnspan=3)
        file_label.grid(column=1, row=0,columnspan=2)
        save_btn.grid(column=1, row=5,columnspan=2)
        
        
    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numberLines.redraw)

    def onScrollRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numberLines.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.numberLines.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        self.numberLines.redraw()


'''THIS CODE IS CREDIT OF Bryan Oakley (With minor visual modifications on my side): 
https://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget'''


class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill="#606366")
            i = self.textwidget.index("%s+1line" % i)


# -- End

class GIFLabel(tk.Label):
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)

def record(sheet):
    #get total elements
    count = len(sheet.get_children())+1
    #create a new entry
    id_new = "Macro_"+str(count)
    print(id_new)
    id2 = sheet.insert("", "end", id_new, text=id_new)
    sheet.insert(id2, "end", text="Loop", values=("0"))
    sheet.insert(id2, "end", text="Scheduled Time", values=("NA"))
    #call listener from macro
    macro.listener(id_new)
#    top = Toplevel()
#    top.title('Writing Code')
#    top.deiconify()
#    lbl = GIFLabel(top)
#    lbl.pack()
#    lbl.load('loading.gif')
#    top.transient(root)
#    top.grab_set()
#    top.after(100000, top.destroy)
#    root.wait_window(top)
    
    
    
def create_code(sheet):
    file_name = ""
    for item in sheet.selection():
            item_text = sheet.item(item,"text")
            file_name =item_text
    print(file_name)
    if file_name != "":
        macro.create_code(file_name)
    else:
        top_error = Toplevel()
        top_error
    top = Toplevel()
    top.title('Writing Code')
    top.deiconify()
    lbl = GIFLabel(top)
    lbl.pack()
    lbl.load('loading.gif')
    top.transient(root)
    top.grab_set()
    top.after(6000, top.destroy)
    root.wait_window(top)
    
def run_code(sheet):
    file_name = ""
    for item in sheet.selection():
            item_text = sheet.item(item,"text")
            file_name =item_text
    print(file_name)
    macro.run_code(file_name)


# --! Table Macro operations
def delete_macro(sheet):
    selected_item = sheet.selection()[0] ## get selected item
    if "Macro_" in selected_item:
        sheet.delete(selected_item)
        
def open_code(sheet):
    configfile.delete(1.0,"end")
    selected_item = sheet.selection()[0] ## get selected item
    if "Macro_" in selected_item:
        code_file = "../files/"+selected_item+".py"
        with open(code_file, 'r') as f:
            configfile.insert(INSERT, f.read())
            
            
def open_file(sheet):
    configfile.delete(1.0,"end")
    selected_item = sheet.selection()[0] ## get selected item
    if "Macro_" in selected_item:
        code_file = "../files/"+selected_item+".txt"
        with open(code_file, 'r') as f:
            configfile.insert(INSERT, f.read())
    
# ---! Menu Bar Code
def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing)

editmenu.add_separator()

editmenu.add_command(label="Cut", command=donothing)
editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
editmenu.add_command(label="Delete", command=donothing)
editmenu.add_command(label="Select All", command=donothing)

menubar.add_cascade(label="Edit", menu=editmenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)


# ---! END


# ---! Code for Record, Create Code, Play buttons -- top left frame
frame_top_left = ttk.Frame(content_top, borderwidth=5, relief="flat", width=380, height=135)


code_btn_icon = PhotoImage(file="./icons/codeF2.png")
create_Code = Button(frame_top_left, text = "Create Code",image=code_btn_icon,compound="top", command = lambda: create_code(table_macro))#,state=tk.DISABLED)

play_btn_icon = PhotoImage(file="./icons/play2.png")
play_Code = Button(frame_top_left, text = "Run Code",image=play_btn_icon,compound="top",command = lambda: run_code(table_macro))#,state=tk.DISABLED)

record_btn_icon = PhotoImage(file="./icons/record3.png")
record_btn = Button(frame_top_left, text = "Record",image=record_btn_icon,compound="top", command = lambda: record(table_macro))#macro.listener)


content_top.grid(column=0, row=0)
frame_top_left.grid(column=0, row=0, columnspan=3, rowspan=1,padx=60)
record_btn.grid(column=0, row=0,padx=5,pady=5)
create_Code.grid(column=1, row=0,padx=5,pady=5)
play_Code.grid(column=2, row=0,padx=5,pady=5)


# ---! END


# ---! Code for Macro List and buttons -- bottom left
frame_bottom_left = ttk.Frame(content_top, borderwidth=5, relief="flat", width=380, height=450)

macro_label_image = PhotoImage(file="./icons/macro_list2.png")
macro_list_label = Label(frame_bottom_left, text="Macro List",image=macro_label_image,compound="left")

scrollbar = Scrollbar(frame_bottom_left)


#style = ttk.Style()
#style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) 
#style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) 
#style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders



table_macro = ttk.Treeview(frame_bottom_left,height=15,style="mystyle.Treeview")
table_macro["columns"] = ("one")
table_macro.column("one", width=250)
table_macro.heading("#0", text="Macro")
table_macro.heading("one", text="Value")


del_macro_icon = PhotoImage(file="./icons/typewriter4.png")
del_macro = Button(frame_bottom_left,text="Delete", image=del_macro_icon,compound="top", relief="flat",command=lambda : delete_macro(table_macro))

action_btn_icon = PhotoImage(file="./icons/icons8-timer.png")
action_btn_file = Button(frame_bottom_left,image=action_btn_icon,compound="top", relief="flat",text="Add Enhancement")

open_btn_code_icon = PhotoImage(file="./icons/typewriter.png")
open_btn_code = Button(frame_bottom_left,image=open_btn_code_icon,compound="top", relief="flat",text="Open Code",command=lambda:open_code(table_macro))

open_btn_file_icon = PhotoImage(file="./icons/typewriter2.png")
open_btn_file = Button(frame_bottom_left,image=open_btn_file_icon,compound="top", relief="flat",text="Open Macro",command=lambda:open_file(table_macro))




frame_bottom_left.grid(column=0, row=6, columnspan=4, rowspan=8,pady=40)
macro_list_label.grid(column=0, row=0,columnspan=2)
table_macro.grid(column=0,row=1,padx=20, columnspan=4,rowspan=4)#padx=40,
del_macro.grid(column=0, row=7,padx=20,pady=5)
action_btn_file.grid(column=1, row=7,padx=20,pady=5)
open_btn_code.grid(column=2, row=7,padx=20,pady=5)
open_btn_file.grid(column=3, row=7,padx=20,pady=5)


# ---! END


# ---! Code for Mouse, Keyboard, Sleep buttons -- top middle frame
frame_top_middle = ttk.Frame(content_top, borderwidth=5, relief="flat", width=500, height=135)


mouse_btn_icon = PhotoImage(file="./icons/icons8-hand-cursor.png")
mouse_btn = Button(frame_top_middle, text = "Insert Mouse Action",image=mouse_btn_icon,compound="top")#, command = threading.Thread(target=create_code).start(),state=tk.DISABLED)

keyboard_btn_icon = PhotoImage(file="./icons/icons8-keyboard-100.png")
keyboard_Code = Button(frame_top_middle, text = "Insert Keyb Action",image=keyboard_btn_icon,compound="top")#, command = threading.Thread(target=run_code).start(),state=tk.DISABLED)

sleep_btn_icon = PhotoImage(file="./icons/icons8-pocket-watch-100.png")
sleep_btn = Button(frame_top_middle , text = "Insert Wait",image=sleep_btn_icon,compound="top")# command = threading.Thread(target=listen_to_me).start())

separator = PhotoImage(file="./icons/icons8-vertical-line.png")
separator_label = Label(frame_top_left,image=separator,compound="left")


frame_top_middle.grid(column=4, row=0, columnspan=3, rowspan=1)
#.separator_label.grid(column=4, row=0,padx=5,pady=5)
mouse_btn.grid(column=1, row=0,padx=5,pady=5)
keyboard_Code.grid(column=2, row=0,padx=5,pady=5)
sleep_btn.grid(column=3, row=0,padx=5,pady=5)
# ---! END


# ---! Code for Code Viewer, Keyboard, Sleep buttons -- top middle frame

frame_bottom_middle = ttk.Frame(content_top, borderwidth=5, relief="flat", width=380, height=450)
configfile = ScrollText(frame_bottom_middle)


frame_bottom_middle.grid(column=4, row=6, columnspan=3, rowspan=8,pady=40)
#file_label.grid(column=0, row=0,columnspan=2)
configfile.grid(column=1,row=0,padx=40, columnspan=1,rowspan=1)
#save_btn.grid(column=1, row=7,padx=5,pady=5)

#del_macro.grid(column=0, row=7,padx=20,pady=5)
#open_btn.grid(column=1, row=7,padx=20,pady=5)

#configfile.grid(column=1, row=1,columnspan=3,padx=5,pady=5)


root.mainloop()