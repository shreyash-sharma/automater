from pynput.keyboard import Listener  as KeyboardListener
from pynput.mouse    import Listener  as MouseListener
from pynput.keyboard import Key
import sys
import datetime
from datetime import date
from pynput import keyboard
import pyautogui
import time 
import pyHook 
from threading import Timer
import win32gui
import logging

class blockInput():
    def OnKeyboardEvent(self,event):
        return False

    def OnMouseEvent(self,event):
        return False

    def unblock(self):
        logging.info(" -- Unblock!")
        if self.t.is_alive():
            self.t.cancel()
        try: self.hm.UnhookKeyboard()
        except: pass
        try: self.hm.UnhookMouse()
        except: pass

    def block(self, timeout = 10, keyboard = True, mouse = True):
        self.t = Timer(timeout, self.unblock)
        self.t.start()

        logging.info(" -- Block!")
        if mouse:
            self.hm.MouseAll = self.OnMouseEvent
            self.hm.HookMouse()
        if keyboard:
            self.hm.KeyAll = self.OnKeyboardEvent
            self.hm.HookKeyboard()
        win32gui.PumpWaitingMessages()

    def __init__(self):
        self.hm = pyHook.HookManager()

def listener(file_name):
    today = date.today()
    file = "../files/"+file_name+".txt"
    macro = open(file,"w")
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
        if fun == 'move':
            macro.write(str(datetime.datetime.now().replace(microsecond=0)).replace(str(today),"").strip()+'!__move__({0}, {1}, {2})'.format(value[0],value[1])+"\n")
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
            #sys.exit()
            listener.stop()
            
            
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
        
        
    def after_click(x,y):
        pass
        
    def on_move(x, y):
        #logging.info("pyautogui.move({0}, {1})".format(x, y))
        x = x-50
        y = y-50
        im3 = pyautogui.screenshot(r"D:\Library\Project\Project\theautomater\src\macro\prett.png",region=(x,y, 100 , 100))
    
    def on_click(x, y, button, pressed):
#        block = blockInput()
#        block.block()
#    
#        t0 = time.time()
#        while time.time() - t0 < 2:
#            time.sleep(1)
#            print(time.time() - t0)
#    
#        block.unblock()
        if pressed:
            on_release("clicked")
            button = str(button).replace("Button.","")
            inverted_comma = "'"
            button = f"{inverted_comma}{button}{inverted_comma}"
            mouse_values = [x, y, button]
            macro_writer('click',mouse_values)
            
#        image based click
        time.sleep(1)
        pyautogui.moveTo(1,1)
#        time.sleep(10)
        print(x,y)
        x = x-50
        y = y-50
        im3 = pyautogui.screenshot(r"D:\Library\Project\Project\theautomater\src\macro\prett2.png",region=(x,y, 100 , 100))
        
    def on_scroll(x, y, dx, dy):
        #logging.info('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))
        pass
    
    
    with MouseListener(on_click=on_click, on_move=on_move) as listener:
        with KeyboardListener(on_release=on_release) as listener:
            listener.join()
            
        
    macro.close()
    
if __name__ ==  "__main__":
    listener("image")

