# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 10:10:28 2021

@author: shrey
"""


import pythoncom, pyHook 

def uMad(event):
    return False

hm = pyHook.HookManager()
hm.MouseAll = uMad
hm.KeyAll = uMad
hm.HookMouse()
hm.HookKeyboard()
pythoncom.PumpMessages()