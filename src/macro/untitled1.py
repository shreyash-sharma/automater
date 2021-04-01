import pyautogui
start = pyautogui.locateCenterOnScreen('prett.png')#If the file is not a png file it will not work
print(start)
pyautogui.moveTo(start)