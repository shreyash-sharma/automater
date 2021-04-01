import pyautogui
from time import sleep
def __write__(key):
    pyautogui.typewrite(key)
def __hotkey__(key1,key2):
    pyautogui.hotkey(key1,key2)
def __click__(x1,y1,click):
    pyautogui.click(x=x1,y=y1,button=click)
__click__(300, 1060, 'left')
sleep(5)
__write__(['p', 'r', 'e', 's', 's', 'e', 'd'])
sleep(1)
__write__(['esc'])
