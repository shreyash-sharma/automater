# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 18:16:13 2021

@author: shrey
"""

import pyautogui
import time


#time.sleep(5)
button7location = pyautogui.locateOnScreen('prett2.png',region=(764,900, 1000, 1000),grayscale="True")
print(button7location)


pyautogui.moveTo(764,900)