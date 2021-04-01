# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 19:50:57 2020

@author: shrey
"""


from tkinter import *
from tkinter import ttk
from tksheet import Sheet
import sys
sys.path.append('..')

root = Tk()
root.geometry("1000x700")

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



# ---! Code for Record, Create Code, Play buttons -- top left frame
content_top = ttk.Frame(root)
frame_top_left = ttk.Frame(content_top, borderwidth=5, relief="flat", width=380, height=135)


code_btn_icon = PhotoImage(file="./icons/codeF2.png")
create_Code = Button(frame_top_left, text = "Create Code",image=code_btn_icon,compound="top")#, command = threading.Thread(target=create_code).start(),state=tk.DISABLED)

play_btn_icon = PhotoImage(file="./icons/play2.png")
play_Code = Button(frame_top_left, text = "Run Code",image=play_btn_icon,compound="top")#, command = threading.Thread(target=run_code).start(),state=tk.DISABLED)

record_btn_icon = PhotoImage(file="./icons/record3.png")
record_btn = Button(frame_top_left, text = "Record",image=record_btn_icon,compound="top")# command = threading.Thread(target=listen_to_me).start())


content_top.grid(column=0, row=0)
frame_top_left.grid(column=0, row=0, columnspan=3, rowspan=1)
record_btn.grid(column=0, row=0,padx=5,pady=5)
create_Code.grid(column=1, row=0,padx=5,pady=5)
play_Code.grid(column=2, row=0,padx=5,pady=5)


# ---! END


# ---! Code for Macro List and buttons -- bottom left
frame_bottom_left = ttk.Frame(content_top, borderwidth=5, relief="flat", width=380, height=450)

macro_label_image = PhotoImage(file="./icons/macro_list2.png")
macro_list_label = Label(frame_bottom_left, text="Macro List",image=macro_label_image,compound="left")

scrollbar = Scrollbar(frame_bottom_left)
table_macros = Listbox(frame_bottom_left,height=20,width=60, yscrollcommand = scrollbar.set )

table_macros.insert(END, "a list entry")
table_macros.insert(END, "a list 1")
table_macros.insert(END, "a list 2")
table_macros.insert(END, "a list 2")
table_macros.insert(END, "a list 2")
table_macros.insert(END, "a list 2")


del_macro_icon = PhotoImage(file="./icons/typewriter4.png")
del_macro = Button(frame_bottom_left,text="Delete", image=del_macro_icon,compound="top", relief="flat",
           command=lambda table_macros=table_macros: table_macros.delete(ANCHOR))

open_btn_code_icon = PhotoImage(file="./icons/typewriter.png")
open_btn_code = Button(frame_bottom_left,image=open_btn_code_icon,compound="top", relief="flat",text="Open Code")

open_btn_file_icon = PhotoImage(file="./icons/typewriter2.png")
open_btn_file = Button(frame_bottom_left,image=open_btn_file_icon,compound="top", relief="flat",text="Open Macro")

frame_bottom_left.grid(column=0, row=6, columnspan=3, rowspan=8,pady=40)
macro_list_label.grid(column=0, row=0,columnspan=2)
table_macros.grid(column=0,row=1,padx=40, columnspan=3,rowspan=3)
del_macro.grid(column=0, row=7,padx=20,pady=5)
open_btn_code.grid(column=1, row=7,padx=20,pady=5)
open_btn_file.grid(column=2, row=7,padx=20,pady=5)
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

file_label_image = PhotoImage(file="./icons/macro_list2.png")
file_label = Label(frame_bottom_middle, text="File",image=file_label_image,compound="left")

save_btn_icon = PhotoImage(file="./icons/icons8-save-50.png")
save_btn = Button(frame_bottom_middle , text = "Save",image=save_btn_icon,compound="top", relief="flat")

#scrollbar = Scrollbar(frame_bottom_left)
configfile = Text(frame_bottom_middle, wrap=WORD, width=45, height= 20)
 

with open("chem_data.txt", 'r') as f:
    configfile.insert(INSERT, f.read())


frame_bottom_middle.grid(column=4, row=6, columnspan=3, rowspan=8,pady=40)
file_label.grid(column=0, row=0,columnspan=2)
configfile.grid(column=0,row=1,padx=40, columnspan=3,rowspan=3)
save_btn.grid(column=1, row=7,padx=5,pady=5)

#del_macro.grid(column=0, row=7,padx=20,pady=5)
#open_btn.grid(column=1, row=7,padx=20,pady=5)

#configfile.grid(column=1, row=1,columnspan=3,padx=5,pady=5)


root.mainloop()