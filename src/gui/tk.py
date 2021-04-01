from tkinter import *

from tkinter import messagebox

from pynput.keyboard import Listener  as KeyboardListener
from pynput.mouse    import Listener  as MouseListener
from pynput.keyboard import Key
import sys
import datetime
from datetime import date
from pynput import keyboard
import threading

from datetime import date
today = date.today()
import datetime


import pyautogui
from time import sleep

import subprocess


top = Tk()
top.geometry("600x300")
def listen_to_me():
    if Code["state"] == "normal":
        Code["state"] = "disabled"
    today = date.today()
    macro = open("pyauto.txt","w")
    #logging.basicConfig(filename=("pyauto.txt"), level=logging.DEBUG)#, format='%(asctime)s: %(message)s')
    
    stack = []
    
    
    ctrl_keys = {'\x01' : "'ctrl', 'A'",
    '\x02' : "'ctrl','B'",   
    '\x03' : "'ctrl','C'",   
    '\x04' : "'ctrl','D'",   
    '\x05' : "'ctrl','E'",   
    '\x06' : "'ctrl','F'",   
    '\x07' : "'ctrl','G'",   
    '\x08' : "'ctrl','H'",
    '\x0A' : "'ctrl','J'",
    '\x0B' : "'ctrl','K'",
    '\x0C' : "'ctrl','L'",
    '\x0D' : "'ctrl','M'",
    '\x0E' : "'ctrl','N'",
    '\x0F' : "'ctrl','O'",
    '\x10' : "'ctrl','P'",
    '\x11' : "'ctrl','Q'",
    '\x12' : "'ctrl','R'",
    '\x13' : "'ctrl','S'",
    '\x14' : "'ctrl','T'",
    '\x15' : "'ctrl','U'",
    '\x16' : "'ctrl','V'",
    '\x17' : "'ctrl','W'",
    '\x18' : "'ctrl','X'",
    '\x19' : "'ctrl','Y'",
    '\x1A' : "'ctrl','Z'",
    '\x1B' : "'ctrl',''",
    '\x1C' : "'ctrl','\\'",
    '\x1D' : "'ctrl',''",
    '\x1E' : "'ctrl','^'",
    '\x1F' : "'ctrl','_'",
    '\x7F' : "'ctrl','?'"}
    
    
    def macro_writer(fun,value):
        if fun == 'write':
            macro.write(str(datetime.datetime.now().replace(microsecond=0)).replace(str(today),"").strip()+'!__write__({0})'.format(value)+"\n")
        if fun == 'hot_key_ctrl':
            macro.write(str(datetime.datetime.now().replace(microsecond=0)).replace(str(today),"").strip()+'!__hotkey__({0})'.format(ctrl_keys[value])+"\n")
        if fun == 'click':
            macro.write(str(datetime.datetime.now().replace(microsecond=0)).replace(str(today),"").strip()+'!__click__({0}, {1}, {2})'.format(value[0],value[1],value[2])+"\n")
        if fun == 'hot_key_alt':
            macro.write(str(datetime.datetime.now().replace(microsecond=0)).replace(str(today),"").strip()+'!__hotkey__({0}, {1})'.format(value[0],value[1])+"\n")
        
    def on_release(key):
        prefix = "['"
        suffix = "']"
        print(str(key))
        ctrl_key = str(key)
        key = str(key).replace("'","")
        #if "Key" is not recorded by listener you append everything in stack
        if key.find("Key") == -1:
            stack.append(key)
        print(stack)
        #if "esc" is pressed, to end the listener
        if key == str(Key.esc):
            if "esc" in stack:
            	stack.remove("esc")
                  
        #if there are recorded key strokes in the stack they will be written in the file
            if len(stack) > 0:
                macro_writer('write',stack)
                stack.clear()
            sys.exit()
            
            
        #if any special key is pressed then the stack will be written in the file
        if key.find("Key") != -1:
            print(stack)
            key =  key.replace("Key.","")
            key = f"{prefix}{key}{suffix}"
            #this is to remove "clicked" keyword from stack as it refers to mouse key being pressed
            if "clicked" in stack:
            	stack.remove("clicked")
                
           
            
            #implementation of alt key with others
            if key == "['alt_l']" or key == "['alt_r']":
                if len(stack) > 0: #checking if atleast one element is present in stack that was pressed with alt
                    last_element = stack[-1] #last element of stack
                    stack.remove(stack[-1])
                    if len(stack) > 0:
                        macro_writer('write',stack)
                        stack.clear()
                    alt_keys = ["'alt'",repr(last_element)]
                    macro_writer('hot_key_alt',alt_keys)
                    
                
            if len(stack) > 0:
                macro_writer('write',stack)
                stack.clear() 
    
            #removing shift,alt keys from stack
            if key != "['shift']" and key != "['alt_l']" and key != "['alt_r']" and key != "['ctrl_l']" and key != "['ctrl_r']":
                macro_writer('write',key)
            
        #if mouse is clicked the stack is written in the file and emptied
        if key == "clicked":
            print(stack)
            stack.remove("clicked")
            if len(stack) > 0:
                macro_writer('write',stack)
                stack.clear()
        
        
        
        
        
        #implementation of ctrl key with others
        #if a ctrl key is pressed in association to any other key we are iterating ctrl_keys to find the relevant key and write it in the file
        for index, key in enumerate(ctrl_keys):
            if repr(key) == ctrl_key:
                print(ctrl_key)
                ctrl_key = str(ctrl_key).replace("'","")
                if ctrl_key in stack:
                    stack.remove(ctrl_key)
                if "clicked" in stack:
                    stack.remove("clicked")
                if len(stack) > 0:
                    macro_writer('write',stack)
                    stack.clear()
                macro_writer('hot_key_ctrl',key)
        
        #check for capslock -- to be implemented
        
        
        
        
    def on_move(x, y):
        #logging.info("pyautogui.move({0}, {1})".format(x, y))
        pass
    
    def on_click(x, y, button, pressed):
        if pressed:
            on_release("clicked")
            button = str(button).replace("Button.","")
            inverted_comma = "'"
            button = f"{inverted_comma}{button}{inverted_comma}"
            mouse_values = [x, y, button]
            macro_writer('click',mouse_values)
    def on_scroll(x, y, dx, dy):
        #logging.info('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))
        pass
    
    
    with MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        with KeyboardListener(on_release=on_release) as listener:
            listener.join()
            
        
    macro.close()
    if (Code['state'] == tk.DISABLED):
        Code['state'] = tk.NORMAL


def create_code():
    writ = open("macros.py", "w")
    
    writ.write("import pyautogui"+"\n")
    writ.write("from time import sleep"+"\n")
    writ.write("def __write__(key):"+"\n")
    writ.write("    pyautogui.typewrite(key)"+"\n")
    writ.write("def __hotkey__(key1,key2):"+"\n")
    writ.write("    pyautogui.hotkey(key1,key2)"+"\n")
    writ.write("def __click__(x1,y1,click):"+"\n")
    writ.write("    pyautogui.click(x=x1,y=y1,button=click)"+"\n")
    
    
    f = open("pyauto.txt")
    Lines = f.readlines()
    count = 0
    # Strips the newline character 
    for idx,line in enumerate(Lines):
        #print(Lines[idx+0])
        line=Lines[idx]
        a=int(len(line))
        last = line.find("!")
        time_current = line[0:last].split(":")
        writ.write(line[last+1:a])
        if idx < len(Lines)-1:
            line_next=Lines[idx+1]
            last = line_next.find("!")
            time_next = line_next[0:last].split(":")
            
            #sleep logic
            if int(time_next[1]) > int(time_current[1]):
                diff = int(time_next[1]) - int(time_current[1])
                diff = 60 * diff
                time_next[2] = int(time_next[2]) + diff
            sleep = (int(time_next[2])-int(time_current[2]))
            if sleep == 0:
                sleep = 1
            writ.write("sleep("+str(sleep)+")"+"\n")
        #pp = pp.replace(pp[0:last], "") 
    
        
    writ.close()
    if (Run_Code['state'] == tk.DISABLED):
        Run_Code['state'] = tk.NORMAL
        
def run_code():
    subprocess.call("python macros.py 1", shell=True)


Code = Button(top, text = "Create Code", command = threading.Thread(target=create_code).start(),state=tk.DISABLED)
Run_Code = Button(top, text = "Run Code", command = threading.Thread(target=run_code).start(),state=tk.DISABLED)

Listener = Button(top, text = "Listener", command = threading.Thread(target=listen_to_me).start())
Listener.place(x = 50,y = 50)
Code.place(x = 150,y = 50)
Run_Code.place(x = 350,y = 50)
top.mainloop()