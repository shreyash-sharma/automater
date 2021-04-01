import pyautogui
from time import sleep
def __write__(key):
    pyautogui.typewrite(key)
def __hotkey__(key1,key2):
    pyautogui.hotkey(key1,key2)
def __click__(x1,y1,click):
    pyautogui.click(x=x1,y=y1,button=click)
__click__(144, 219, 'left')
sleep(4)
__click__(167, 1069, 'left')
sleep(6)
__write__(['y', 'u', 'p'])
sleep(1)
__write__(['esc'])
